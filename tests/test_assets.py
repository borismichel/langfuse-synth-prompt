from collections import Counter
from types import SimpleNamespace

import pytest

from synth.assets import (AssetConflict, chat_prompt, bind_historical_experiments,
                          configure_evaluators, provision_assets, rule_body, variable_mapping)
from synth.catalog import load_fixture, score_definitions, system_prompt


class FakeAPI:
    def __init__(self, collision=None, connected=True):
        self.writes = []
        self.collision = collision
        self.connected = connected
        self.versions = Counter()
        self.created = {}

    def read(self, path, params=None):
        if path in self.created:
            return self.created[path]
        if path in {"/api/public/v2/evaluators", "/api/public/v2/evaluation-rules"}:
            return {"data": [v for k, v in self.created.items() if k.rsplit("/", 1)[0] == path]}
        if path == "/api/public/dataset-items":
            return {"data": [v for k, v in self.created.items() if k.startswith(path + "/") and v["datasetName"] == params["datasetName"]]}
        if path == "/api/public/projects":
            return {"data": [{"id": "project-test"}]}
        if path == "/api/public/llm-connections":
            return {"data": [{"provider": "openai", "withDefaultModels": True}] if self.connected else []}
        if self.collision and path == self.collision[0]:
            # A later-page collision must still be caught before any writes.
            if params.get("page", 1) == 1:
                return {"data": [{"name": f"unrelated-{i}"} for i in range(100)], "meta": {"totalPages": 2}}
            return {"data": [{"name": self.collision[1]}]}
        return {"data": [], "meta": {}}

    def create(self, path, body):
        self.writes.append((path, body))
        result = {**body, "id": str(len(self.writes))}
        if path == "/api/public/v2/prompts":
            self.versions[body["name"]] += 1
            result["version"] = self.versions[body["name"]]
        if path == "/api/public/v2/evaluators":
            result.update(version=1, versionId="version-" + result["id"], status="active")
        if path == "/api/public/dataset-items":
            from datetime import datetime, timedelta, timezone
            result["updatedAt"] = (datetime(2026, 10, 8, tzinfo=timezone.utc) + timedelta(seconds=len(self.writes))).isoformat()
        self.created[path + "/" + result["id"]] = result
        return result


def config(evals=True):
    return SimpleNamespace(target=SimpleNamespace(base_url="https://example.invalid"),
                           evaluation=SimpleNamespace(provider="openai" if evals else "", model="test-model" if evals else ""),
                           live=SimpleNamespace(model="test-model"))


@pytest.mark.parametrize("path,name", [
    ("/api/public/v2/prompts", "products/explainer"),
    ("/api/public/v2/datasets", "prompt/DS-01-products-explainer"),
    ("/api/public/score-configs", "dark_side_delivery"),
])
def test_any_collision_on_later_page_prevents_all_writes(path, name):
    api = FakeAPI((path, name))
    with pytest.raises(AssetConflict):
        provision_assets(config(), api=api)
    assert api.writes == []


def test_full_assets_are_model_free_and_follow_accepted_story():
    api = FakeAPI()
    receipt = provision_assets(config(), api=api)
    counts = Counter(path for path, _ in api.writes)
    assert counts == {
        "/api/public/models": 3, "/api/public/score-configs": 12,
        "/api/public/v2/prompts": 72, "/api/public/v2/datasets": 9,
        "/api/public/dataset-items": 32,
    }
    assert receipt["evaluators"] == receipt["evaluator_rules"] == {}
    assert not {"E-02", "E-03"} & receipt["evaluators"].keys()
    assert any("inapplicability" in x for x in receipt["missing"])
    assert all("protected" not in x for x in receipt["missing"])
    assert receipt["manual_prerequisites"]
    for dataset in receipt["datasets"].values():
        assert dataset["version"] == max(i["server_updated_at"] for i in dataset["items"])
    for name in api.versions:
        versions = [b for p, b in api.writes if p.endswith("/prompts") and b["name"] == name]
        assert versions[6]["labels"] == ["production"]
        assert versions[7]["labels"] == ["development"]
        assert all("production" not in b["labels"] for i, b in enumerate(versions) if i != 6)
    assert chat_prompt("PR-01", 7)[0]["content"] == system_prompt("PR-01", 7)
    for path, body in api.writes:
        if path.endswith("evaluation-rules"):
            assert body["filter"][0]["value"] == ["prompt-live"]
            assert body["enabled"] is True
        if path.endswith("dataset-items"):
            assert "evaluation_context" in body["metadata"]


def test_eval_setup_is_separate_reusable_and_seed_never_creates_evaluators():
    api = FakeAPI()
    configured = configure_evaluators(config(), api=api)
    assert len(configured["evaluators"]) == 8
    assert len(configured["evaluator_rules"]) == 8
    assert all(path in {"/api/public/v2/evaluators", "/api/public/v2/evaluation-rules"} for path, _ in api.writes)
    writes = len(api.writes)
    assert configure_evaluators(config(), api=api) == configured
    assert len(api.writes) == writes
    seeded = provision_assets(config(), api=api)
    assert seeded["evaluators"] == configured["evaluators"]
    assert not any("evaluat" in path for path, _ in api.writes[writes:])


def test_conflicting_existing_evaluator_aborts_without_any_setup_writes():
    api = FakeAPI()
    configure_evaluators(config(), api=api)
    identifier = next(k for k in api.created if k.startswith("/api/public/v2/evaluators/"))
    api.created[identifier]["prompt"] = "Different rubric"
    before = len(api.writes)
    with pytest.raises(AssetConflict, match="conflicts"):
        configure_evaluators(config(), api=api)
    assert len(api.writes) == before


@pytest.mark.parametrize("configured,connected", [(False, True), (True, False)])
def test_missing_provider_never_creates_managed_evals(configured, connected):
    api = FakeAPI(connected=connected)
    receipt = provision_assets(config(configured), api=api)
    assert receipt["evaluators"] == receipt["evaluator_rules"] == {}
    assert receipt["missing"]
    assert not any("evaluat" in p for p, _ in api.writes)


def test_input_only_mappings_cannot_see_reply_and_reply_rubric_is_scoped():
    for eid in ["E-05", "E-06", "E-07", "E-08"]:
        for live in [True, False]:
            assert all(m["source"] != "output" for m in variable_mapping(eid, live=live))
    assert variable_mapping("E-07", live=True) == [{"variable": "current_user_message", "source": "metadata", "jsonPath": "$.current_user_message"}]
    rule = rule_body("E-01", score_definitions()["E-01"], "eval-1", load_fixture("portfolio")["prompts"])
    assert rule["filter"][2]["value"] == ["PR-01"]
    assert all(m["source"] == "experiment_item_metadata" for m in variable_mapping("E-05", live=False))


def test_history_binding_is_pure_preserves_time_and_score_targets():
    import copy
    from datetime import datetime, timezone
    from synth.materialize import build_historical_experiment_events
    api = FakeAPI()
    receipt = provision_assets(config(False), api=api)
    events, links = build_historical_experiment_events({"seed": 42}, run_date=datetime(2026, 10, 8, tzinfo=timezone.utc))
    before = copy.deepcopy(events)
    bound, result = bind_historical_experiments(events, receipt, links)
    assert events == before
    assert len(bound) == len(events)
    assert len(result) == 18
    assert bind_historical_experiments(events, receipt, links) == (bound, result)
    for old, new in zip(events, bound):
        if "spanId" not in old:
            assert old == new
            continue
        assert old["traceId"] == new["traceId"] and old["spanId"] == new["spanId"]
        assert old["startTimeUnixNano"] == new["startTimeUnixNano"]
        attrs = {a["key"]: a["value"]["stringValue"] for a in new["attributes"] if "stringValue" in a["value"]}
        expected = next(l for l in result if l["trace_id"] == new["traceId"])
        assert attrs["langfuse.experiment.item.root_observation_id"] == expected["observation_id"]
        assert attrs["langfuse.experiment.dataset.id"] == expected["dataset_id"]
        if new["spanId"] == expected["observation_id"]:
            import json
            context = json.loads(attrs["langfuse.experiment.item.metadata.evaluation_context"])
            assert set(context) == {"current_user_message", "prior_messages", "reference_context"}
    with pytest.raises(ValueError, match="already bound"):
        bind_historical_experiments(bound, receipt, links)


def test_invalid_history_reference_cannot_change_spool():
    api = FakeAPI()
    receipt = provision_assets(config(False), api=api)
    with pytest.raises(StopIteration):
        bind_historical_experiments([], receipt,
            [{"prompt_id": "PR-01", "case_id": "unknown", "trace_id": "x"}])
