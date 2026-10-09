"""Explicit model and naming policy migration preserves rubrics and base prices."""
from copy import deepcopy

import pytest

from synth.assets import AssetAPI, AssetConflict, configure_evaluators, ensure_policy_models
from synth.model_policy import MODEL_PRICES
from test_assets import FakeAPI, config


class PolicyAPI(FakeAPI):
    def __init__(self):
        super().__init__()
        self.updates = []
        self.reads = []
        self.fail_update = None
        self.corrupt_readback = False

    def read(self, path, params=None):
        self.reads.append(path)
        if path == "/api/public/models":
            return {"data": [value for key, value in self.created.items()
                             if key.startswith(path + "/")]}
        return deepcopy(super().read(path, params))

    def update(self, path, body):
        self.updates.append((path, deepcopy(body)))
        if len(self.updates) == self.fail_update:
            raise TimeoutError("Ambiguous update")
        old = self.created[path]
        current = {**old, **deepcopy(body)}
        if "/evaluators/" in path:
            current.update(version=old["version"] + 1,
                           versionId=old["versionId"] + "-next", status="active")
        if self.corrupt_readback:
            current["status"] = "paused"
        self.created[path] = current
        return deepcopy(current)


def existing_judges():
    api = PolicyAPI()
    receipt = configure_evaluators(config(), api=api)
    api.writes.clear()
    api.reads.clear()
    cfg = config()
    cfg.evaluation.model = "claude-sonnet-5-5"
    return api, cfg, receipt


def test_model_change_requires_explicit_flag_and_reads_all_before_any_write():
    api, cfg, original = existing_judges()
    with pytest.raises(AssetConflict, match="conflicts"):
        configure_evaluators(cfg, api=api)
    assert api.writes == api.updates == []
    original_resources = deepcopy(api.created)
    original_update = api.update

    def checked_update(path, body):
        assert all("/api/public/v2/evaluators/" + e["id"] in api.reads
                   for e in original["evaluators"].values())
        assert set(body) == {"name", "type", "description", "prompt", "modelConfig", "variableMapping", "outputDefinition"}
        original_update(path, body)

    api.update = checked_update
    result = configure_evaluators(cfg, api=api, update_model=True)
    assert len(api.updates) == 10
    assert api.writes == []
    assert result["evaluator_rules"] == original["evaluator_rules"]
    for eid, previous in original["evaluators"].items():
        current = result["evaluators"][eid]
        assert current["id"] == previous["id"]
        assert current["version"] == 2
        assert current["version_id"] == previous["version_id"] + "-next"
    for path, previous in original_resources.items():
        if "/evaluation-rules/" in path:
            assert api.created[path] == previous
        else:
            for key, value in previous.items():
                if key not in {"modelConfig", "version", "versionId"}:
                    assert api.created[path][key] == value
    assert configure_evaluators(cfg, api=api, update_model=True) == result
    assert len(api.updates) == 10


@pytest.mark.parametrize("field,bad", [
    ("prompt", "Changed rubric"), ("description", "Unapproved change"),
    ("variableMapping", []), ("outputDefinition", {"dataType": "NUMERIC"}),
    ("status", "paused"), ("version", None), ("versionId", None),
])
def test_only_model_difference_is_allowed_even_for_last_evaluator(field, bad):
    api, cfg, original = existing_judges()
    last = list(original["evaluators"].values())[-1]
    api.created["/api/public/v2/evaluators/" + last["id"]][field] = bad
    with pytest.raises(AssetConflict):
        configure_evaluators(cfg, api=api, update_model=True)
    assert api.updates == api.writes == []


def test_missing_evaluator_aborts_model_only_update_without_creating_anything():
    api, cfg, original = existing_judges()
    last = list(original["evaluators"].values())[-1]
    del api.created["/api/public/v2/evaluators/" + last["id"]]
    with pytest.raises(AssetConflict, match="existing evaluator"):
        configure_evaluators(cfg, api=api, update_model=True)
    assert api.updates == api.writes == []


def test_model_only_update_does_not_create_missing_rule():
    api, cfg, original = existing_judges()
    last = list(original["evaluator_rules"].values())[-1]
    del api.created["/api/public/v2/evaluation-rules/" + last["id"]]
    result = configure_evaluators(cfg, api=api, update_model=True)
    assert len(api.updates) == 10 and api.writes == []
    assert len(result["evaluator_rules"]) == 9 and len(result["missing"]) == 1


def test_mid_update_failure_stops_without_retry_or_next_write():
    api, cfg, _ = existing_judges()
    api.fail_update = 3
    with pytest.raises(TimeoutError):
        configure_evaluators(cfg, api=api, update_model=True)
    assert len(api.updates) == 3
    assert len({path for path, _ in api.updates}) == 3
    assert api.writes == []


def test_update_readback_must_be_active_before_next_write():
    api, cfg, _ = existing_judges()
    api.corrupt_readback = True
    with pytest.raises(AssetConflict, match="active version"):
        configure_evaluators(cfg, api=api, update_model=True)
    assert len(api.updates) == 1


def test_asset_patch_uses_single_attempt(monkeypatch):
    calls = []
    from langfuse_synth_core import http, lfread
    monkeypatch.setattr(lfread, "auth_from_env", lambda: ("public", "secret"))

    def timeout(*args, **kwargs):
        calls.append((args, kwargs))
        raise TimeoutError("Ambiguous")

    monkeypatch.setattr(http, "request_retry", timeout)
    with pytest.raises(TimeoutError):
        AssetAPI("https://example.invalid").update("/api/public/v2/evaluators/id", {"modelConfig": {}})
    assert len(calls) == 1
    assert calls[0][0][0] == "PATCH" and calls[0][1]["attempts"] == 1


def test_registry_uses_base_prices_and_reuses_exact_models():
    api = PolicyAPI()
    api.created["/api/public/models/old"] = {"id": "old", "modelName": "demo-standard-v1"}
    old = deepcopy(api.created["/api/public/models/old"])
    result = ensure_policy_models(config(), api=api)
    assert set(result) == set(MODEL_PRICES)
    assert len(api.writes) == 3
    for name, receipt in result.items():
        rates = MODEL_PRICES[name]
        assert receipt["input_per_million"] == rates[0]
        assert receipt["output_per_million"] == rates[1]
        current = api.created["/api/public/models/" + receipt["id"]]
        assert current["pricingTiers"][0]["prices"] == {"input": rates[0] / 1e6, "output": rates[1] / 1e6}
    assert ensure_policy_models(config(), api=api) == result
    assert len(api.writes) == 3
    assert api.created["/api/public/models/old"] == old


def test_wrong_registry_prices_abort_preflight_before_creating_missing_models():
    api = PolicyAPI()
    receipt = ensure_policy_models(config(), api=api)
    for name in list(MODEL_PRICES)[:2]:
        del api.created["/api/public/models/" + receipt[name]["id"]]
    last = api.created["/api/public/models/" + receipt[list(MODEL_PRICES)[-1]]["id"]]
    last["pricingTiers"][0]["prices"]["input"] *= 3
    api.writes.clear()
    with pytest.raises(AssetConflict, match="base pricing"):
        ensure_policy_models(config(), api=api)
    assert api.writes == []


def test_cli_model_update_flag_is_explicit():
    from synth.cli import build_parser
    parser = build_parser()
    assert not parser.parse_args(["configure-evaluators", "--config", "config/demo.yaml"]).update_model
    assert parser.parse_args(["configure-evaluators", "--config", "config/demo.yaml", "--update-model"]).update_model


def test_reuse_managed_provider_models_with_cache_and_conditional_tiers():
    api = PolicyAPI()
    for name, rates in MODEL_PRICES.items():
        api.created["/api/public/models/" + name] = {
            "id": name, "modelName": name, "isLangfuseManaged": True, "unit": None,
            "matchPattern": "(?i)^(anthropic/)?" + name + "$",
            "pricingTiers": [
                {"isDefault": True, "conditions": [], "prices": {"input": rates[0]/1e6, "output": rates[1]/1e6, "input_cache_read": 1e-7}},
                {"isDefault": False, "conditions": [{"key": "speed", "values": ["fast"]}], "prices": {"input": rates[0]*2/1e6}},
            ]}
    original = deepcopy(api.created)
    result = ensure_policy_models(config(), api=api)
    assert set(result) == set(MODEL_PRICES)
    assert api.writes == [] and api.created == original
    api.created["/api/public/models/claude-opus-5-5"]["pricingTiers"][0]["prices"]["input"] *= 3
    with pytest.raises(AssetConflict):
        ensure_policy_models(config(), api=api)
    assert api.writes == []


def legacy_judges():
    from synth.catalog import score_definitions
    api, cfg, receipt = existing_judges()
    definitions = score_definitions()
    for eid, anchor in receipt["evaluators"].items():
        evaluator = api.created["/api/public/v2/evaluators/" + anchor["id"]]
        evaluator["description"] = f"Prompt demo {eid}, rubric {definitions[eid]['revision']}; authored rubric, model-executed results."
        rule = api.created["/api/public/v2/evaluation-rules/" + receipt["evaluator_rules"][eid]["id"]]
        rule["name"] = f"prompt/{eid}/live"
        rule["filter"] = [f for f in rule["filter"] if f.get("key") != "evaluation_mode"]
        next(f for f in rule["filter"] if f["column"] == "environment")["value"] = ["prompt-live"]
    return api, cfg, receipt


def test_exact_legacy_policy_migrates_in_place_after_complete_preflight():
    from synth.assets import evaluator_body, rule_body
    from synth.catalog import load_fixture, score_definitions
    api, cfg, original = legacy_judges()
    before = deepcopy(api.created)
    with pytest.raises(AssetConflict):
        configure_evaluators(cfg, api=api)
    assert api.updates == api.writes == []
    update = api.update

    def checked_update(path, body):
        assert set(before) <= set(api.reads)
        update(path, body)

    api.update = checked_update
    result = configure_evaluators(cfg, api=api, update_model=True)
    assert len(api.updates) == 20 and api.writes == [] and not result["missing"]
    assert result["evaluator_rules"] == original["evaluator_rules"]
    definitions, prompts = score_definitions(), load_fixture("portfolio")["prompts"]
    for eid, anchor in original["evaluators"].items():
        path = "/api/public/v2/evaluators/" + anchor["id"]
        current = api.created[path]
        expected = evaluator_body(eid, definitions[eid], cfg.evaluation.provider, cfg.evaluation.model)
        assert {key: current[key] for key in expected} == expected
        assert current["id"] == before[path]["id"]
        for key in ("prompt", "variableMapping", "outputDefinition", "name", "type"):
            assert current[key] == before[path][key]
        path = "/api/public/v2/evaluation-rules/" + original["evaluator_rules"][eid]["id"]
        current = api.created[path]
        expected = rule_body(eid, definitions[eid], anchor["id"], prompts)
        assert {key: current[key] for key in expected} == expected
        assert current["id"] == before[path]["id"]
        assert current["evaluatorAssignments"] == before[path]["evaluatorAssignments"]
    assert configure_evaluators(cfg, api=api, update_model=True) == result
    assert len(api.updates) == 20


@pytest.mark.parametrize("damage", ["environment", "subject", "sampling", "mapping", "identity", "duplicate"])
def test_noncanonical_legacy_rule_blocks_all_updates(damage):
    api, cfg, receipt = legacy_judges()
    eid = list(receipt["evaluator_rules"])[-1]
    rule = api.created["/api/public/v2/evaluation-rules/" + receipt["evaluator_rules"][eid]["id"]]
    if damage == "environment":
        next(f for f in rule["filter"] if f["column"] == "environment")["value"] = ["production"]
    elif damage == "subject":
        next(f for f in rule["filter"] if f.get("key") == "evaluation_subject")["value"] = "wrong-target"
    elif damage == "sampling": rule["sampling"] = .5
    elif damage == "mapping": rule["evaluatorAssignments"][0]["variableMapping"] = []
    elif damage == "identity":
        read = api.read
        path = "/api/public/v2/evaluation-rules/" + rule["id"]
        api.read = lambda requested, params=None: {**read(requested, params), "id": "wrong-id"} if requested == path else read(requested, params)
    elif damage == "duplicate":
        api.created["/api/public/v2/evaluation-rules/duplicate"] = {**deepcopy(rule), "id": "duplicate", "name": f"prompt/{eid}/production"}
    with pytest.raises(AssetConflict):
        configure_evaluators(cfg, api=api, update_model=True)
    assert api.updates == api.writes == []


def test_rule_update_readback_failure_stops_before_next_evaluator():
    api, cfg, _ = legacy_judges()
    update = api.update

    def broken_update(path, body):
        update(path, body)
        if "/evaluation-rules/" in path:
            api.created[path]["filter"] = [f for f in body["filter"] if f.get("key") != "evaluation_mode"]

    api.update = broken_update
    with pytest.raises(AssetConflict, match="Updated rule"):
        configure_evaluators(cfg, api=api, update_model=True)
    assert len(api.updates) == 2 and api.writes == []


def test_production_rules_exclude_all_authored_replays():
    from datetime import datetime, timezone
    from synth.materialize import build_events, build_historical_experiment_events
    from synth.receipt import attributes
    from langfuse_synth_core.seed import otlp
    api, cfg, _ = legacy_judges()
    configured = configure_evaluators(cfg, api=api, update_model=True)
    now = datetime(2026, 10, 9, 12, tzinfo=timezone.utc)
    history = build_events(6, {"seed": 42}, run_date=now)
    experiments, _ = build_historical_experiment_events({"seed": 42}, run_date=now)
    for anchor in configured["evaluator_rules"].values():
        rule = api.created["/api/public/v2/evaluation-rules/" + anchor["id"]]
        assert next(f for f in rule["filter"] if f["column"] == "environment")["value"] == ["production"]
        assert next(f for f in rule["filter"] if f.get("key") == "evaluation_mode") == {
            "type": "stringObject", "column": "metadata", "key": "evaluation_mode", "operator": "=", "value": "online"}
    observations = [e for e in history + experiments if otlp.is_span(e)]
    assert observations
    assert all(attributes(e).get("langfuse.observation.metadata.evaluation_mode") != "online" for e in observations)


def test_fresh_provision_reuses_managed_model_ids_without_changing_tiers():
    from synth.assets import provision_assets
    api = PolicyAPI()
    anchors = ensure_policy_models(config(), api=api)
    for anchor in anchors.values():
        model = api.created["/api/public/models/" + anchor["id"]]
        model["isLangfuseManaged"] = True
        model["pricingTiers"][0]["prices"]["input_cache_read"] = 1e-7
        model["pricingTiers"].append({"isDefault": False, "conditions": [{"key": "speed", "values": ["fast"]}], "prices": {"input": 1e-5}})
    original = deepcopy(api.created)
    api.writes.clear()
    result = provision_assets(config(), api=api)
    assert result["models"] == anchors
    assert not any(path == "/api/public/models" for path, _ in api.writes)
    assert all(api.created[path] == model for path, model in original.items())
