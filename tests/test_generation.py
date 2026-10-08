"""Story assertions through public generation/catalog interfaces; small volume only."""
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
import json

import pytest
from langfuse_synth_core.seed.otlp import finalize, trace_root_span_id

from synth.catalog import (calibration_cases, dataset_items, load_fixture, prompt_by_id,
                           score_definitions, system_prompt)
from synth.materialize import (MODEL_RATES, build_events, build_historical_experiment_events,
                               local_day_bounds, population_plan)


ANCHOR = datetime(2026, 10, 8, tzinfo=timezone.utc)


def attributes(span):
    return {item["key"]: next(iter(item["value"].values())) for item in span["attributes"]}


def metadata(span):
    prefix = "langfuse.observation.metadata."
    result = {}
    for key, value in attributes(span).items():
        if key.startswith(prefix):
            try:
                value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pass
            result[key[len(prefix):]] = value
    return result


@pytest.fixture(scope="module")
def history():
    return finalize(build_events(24, {"seed": 42}, run_date=ANCHOR))


def test_complete_catalog_and_accepted_truth():
    prompts = load_fixture("portfolio")["prompts"]
    assert len(prompts) == 9
    assert sum(p["live_companion"] for p in prompts) == 3
    assert len(score_definitions()) == 12
    for prompt in prompts:
        texts = [system_prompt(prompt["id"], version) for version in range(1, 9)]
        assert len(set(texts)) == 8
        items = dataset_items(prompt["id"])
        assert len(items) == (8 if prompt["id"] == "PR-01" else 3)
        assert all(set(item["input"]) == {"reference_context", "conversation_history", "user_message"} for item in items)
        assert all(item["metadata"]["dataset_version"] == "r1" for item in items)
    product = load_fixture("product")
    assert system_prompt("PR-01", 7) == product["prompt_comparison"]["baseline_system"]
    assert system_prompt("PR-01", 9) == product["prompt_comparison"]["candidate_system"]
    with pytest.raises(ValueError):
        system_prompt("PR-02", 9)
    controls = calibration_cases()
    assert controls[0]["metadata"]["expected_scores"]["E-01"] == 1
    assert controls[0]["metadata"]["expected_scores"]["E-02"] == 0
    assert controls[2]["metadata"]["expected_scores"]["E-03"] is None
    # Caller mutation cannot leak into later source or prompt reads.
    product["source"]["monthly_fee"] = 999
    assert load_fixture("product")["source"]["monthly_fee"] == 4


def test_small_complete_population(history):
    spans = [e for e in history if "spanId" in e]
    scores = [e for e in history if e.get("type") == "score-create"]
    assert len({e["traceId"] for e in spans}) == 24
    assert len(spans) == 60
    assert len(scores) == 138
    assert len({e["spanId"] for e in spans}) == len(spans)
    assert len({e["body"]["id"] for e in scores}) == len(scores)
    gens = [e for e in spans if attributes(e)["langfuse.observation.type"] == "generation"]
    assert len(gens) == 32
    assert {metadata(e)["prompt_id"] for e in gens} == {f"PR-{i:02}" for i in range(1, 10)}
    assert all(int(attributes(e)["langfuse.observation.prompt.version"]) in (1, 3, 5, 6, 7) for e in gens)


def test_scores_evaluate_the_actual_subject_and_context(history):
    spans = {e["spanId"]: e for e in history if "spanId" in e}
    definitions = {d["name"]: d for d in score_definitions().values()}
    scores_by_target = defaultdict(list)
    for event in history:
        if event.get("type") != "score-create":
            continue
        score = event["body"]
        target = spans[score["observationId"]]
        assert target["traceId"] == score["traceId"]
        assert metadata(target)["evaluation_subject"] == definitions[score["name"]]["subject"]
        assert "reference_context" in metadata(target)
        assert "current_user_message" in metadata(target)
        assert "prior_messages" in metadata(target)
        assert "no judge executed" in score["comment"]
        scores_by_target[score["observationId"]].append(score["name"])
    for span in spans.values():
        meta = metadata(span)
        if meta.get("evaluation_subject") == "user_input":
            assert len(scores_by_target[span["spanId"]]) == 4
            assert span["spanId"] == trace_root_span_id(span["traceId"])
            assert "assistant_reply" not in meta
        if meta.get("evaluation_subject") == "assistant_reply":
            assert "assistant_reply" in meta
            assert "user_disagreement" not in scores_by_target[span["spanId"]]


def test_session_replay_and_human_time_are_distinct(history):
    sessions = defaultdict(list)
    for span in history:
        if "spanId" not in span:
            continue
        attrs = attributes(span)
        if "langfuse.session.id" not in attrs:
            continue
        if metadata(span).get("evaluation_subject") == "user_input":
            sessions[attrs["langfuse.session.id"]].append(span)
        else:
            assert attrs["langfuse.observation.type"] == "generation"
    assert len(sessions) == 6
    for turns in sessions.values():
        turns.sort(key=lambda e: int(e["startTimeUnixNano"]))
        previous_messages = []
        for index, root in enumerate(turns):
            assert metadata(root)["prior_messages"] == previous_messages
            user = json.loads(attributes(root)["langfuse.observation.input"])
            assistant = json.loads(attributes(root)["langfuse.observation.output"])
            assert user["role"] == "user" and assistant["role"] == "assistant"
            previous_messages += [user, assistant]
            assert int(root["endTimeUnixNano"]) - int(root["startTimeUnixNano"]) < 3_000_000_000
            if index:
                gap = (int(root["startTimeUnixNano"]) - int(turns[index - 1]["endTimeUnixNano"])) / 1e9
                assert 15 <= gap <= 120 or 300 <= gap <= 1200


def test_flow_three_distinct_links_and_unprompted_lookup(history):
    flows = defaultdict(list)
    for event in history:
        if "spanId" in event and (metadata(event).get("fixture_case_id") == "FLOW-01" or metadata(event).get("operation_id") == "SIM-LOOKUP"):
            flows[event["traceId"]].append(event)
    assert len(flows) == 4
    for operations in flows.values():
        gens = [e for e in operations if attributes(e)["langfuse.observation.type"] == "generation"]
        tools = [e for e in operations if attributes(e)["langfuse.observation.type"] == "tool"]
        assert len(gens) == 3 and len(tools) == 1
        assert {metadata(e)["prompt_id"] for e in gens} == {"PR-04", "PR-05", "PR-09"}
        assert "langfuse.observation.prompt.name" not in attributes(tools[0])
        assert len({e["parentSpanId"] for e in gens + tools}) == 1
    first = next(iter(flows.values()))
    assert all(int(attributes(e)["langfuse.observation.prompt.version"]) == 7 for e in first
               if attributes(e)["langfuse.observation.type"] == "generation")


def test_usage_cost_and_version_periods(history):
    for event in history:
        if "spanId" not in event or attributes(event)["langfuse.observation.type"] != "generation":
            continue
        attrs, meta = attributes(event), metadata(event)
        usage = json.loads(attrs["langfuse.observation.usage_details"])
        cost = json.loads(attrs["langfuse.observation.cost_details"])
        rates = MODEL_RATES[attrs["langfuse.observation.model.name"]]
        assert usage["total"] == usage["input"] + usage["output"]
        assert cost["total"] == pytest.approx((usage["input"] * rates[0] + usage["output"] * rates[1]) / 1e6)
        timestamp = datetime.fromtimestamp(int(event["startTimeUnixNano"]) / 1e9, timezone.utc)
        from zoneinfo import ZoneInfo
        day = (timestamp.astimezone(ZoneInfo("Europe/Berlin")).date() - ANCHOR.date()).days
        version = next(v for v in prompt_by_id(meta["prompt_id"])["versions"] if v["version"] == meta["resolved_version"])
        assert version["relative_days_inclusive"][0] <= day <= version["relative_days_inclusive"][1]


def test_full_scale_is_a_plan_not_an_unperformed_seed():
    plan = population_plan(1620)
    assert {key: plan[key] for key in ("target_traces", "generations", "observations", "outcomes", "chat_turns", "chat_sessions", "chat_users")} == {
        "target_traces": 1620, "generations": 2100, "observations": 3960, "outcomes": 9320,
        "chat_turns": 1080, "chat_sessions": 360, "chat_users": 216}
    assert plan["session_lengths"] == {"PR-01": {2: 72, 3: 72, 5: 36}, "PR-02": {2: 43, 3: 43, 5: 22}, "PR-03": {2: 29, 3: 29, 5: 14}}
    for target in (0, 1, 7, 24, 72, 100, 1620, 5000):
        assert sum(population_plan(target)["request_counts"].values()) == target


def test_dst_and_retargeted_dates():
    spring = local_day_bounds(datetime(2026, 4, 1, tzinfo=timezone.utc), -3)
    autumn = local_day_bounds(datetime(2026, 11, 1, tzinfo=timezone.utc), -7)
    assert spring[1] - spring[0] == timedelta(hours=23)
    assert autumn[1] - autumn[0] == timedelta(hours=25)
    with pytest.raises(ValueError, match="timezone-aware"):
        build_events(1, {}, run_date=datetime(2026, 1, 1))
    events = build_events(7, {"seed": 42}, run_date=ANCHOR + timedelta(days=365))
    lower = local_day_bounds(ANCHOR + timedelta(days=365), -28)[0].timestamp()
    upper = local_day_bounds(ANCHOR + timedelta(days=365), -1)[1].timestamp()
    assert all(lower <= int(e["startTimeUnixNano"]) / 1e9 < upper for e in events if "spanId" in e)


def test_separate_authored_historical_experiments():
    events, links = build_historical_experiment_events({"seed": 42}, run_date=ANCHOR)
    assert len(links) == 18
    assert len(events) == 72
    assert Counter(link["version"] for link in links) == {2: 9, 4: 9}
    assert len({link["run_name"] for link in links}) == 18
    assert all(link["case_id"] == dataset_items(link["prompt_id"])[0]["case_id"] for link in links)
    spans = {e["spanId"]: e for e in events if "spanId" in e}
    for link in links:
        gen = spans[link["observation_id"]]
        assert gen["traceId"] == link["trace_id"]
        assert attributes(gen)["langfuse.environment"] == "experiment"
    for event in events:
        if event.get("type") == "score-create":
            assert metadata(spans[event["body"]["observationId"]])["evaluation_subject"] == "assistant_reply"


def test_seed_and_small_replay_are_deterministic():
    first = build_events(7, {"seed": 19}, run_date=ANCHOR)
    assert first == build_events(7, {"seed": 19}, run_date=ANCHOR)
    assert first != build_events(7, {"seed": 20}, run_date=ANCHOR)
