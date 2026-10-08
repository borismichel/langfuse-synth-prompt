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
from synth.reference_tools import CHAT_OPERATION_NAME, GENERATION_OPERATION_NAME, REFERENCE_RETRIEVER_NAME, FEE_TOOL_NAME


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
    assert controls[0]["metadata"]["expected_scores"]["E-02"] == "Fail"
    assert controls[2]["metadata"]["expected_scores"]["E-03"] == "Not applicable"
    # Caller mutation cannot leak into later source or prompt reads.
    product["source"]["monthly_fee"] = 999
    assert load_fixture("product")["source"]["monthly_fee"] == 4


def test_small_complete_population(history):
    spans = [e for e in history if "spanId" in e]
    scores = [e for e in history if e.get("type") == "score-create"]
    assert len({e["traceId"] for e in spans}) == 24
    assert len(spans) == 77 == population_plan(24)["observations"]
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
            assert attrs["langfuse.observation.type"] in {"generation", "tool", "retriever"}
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


def test_chat_reference_pipeline_matches_model_context_and_session(history):
    traces = defaultdict(list)
    for span in history:
        if "spanId" in span and "langfuse.session.id" in attributes(span):
            traces[span["traceId"]].append(span)
    assert len(traces) == population_plan(24)["chat_turns"] == 16
    source = load_fixture("product")["source"]
    prompts = set()
    calculations = 0
    for trace_id, spans in traces.items():
        by_type = {attributes(span)["langfuse.observation.type"]: span for span in spans}
        assert {"span", "retriever", "generation"} <= by_type.keys()
        root, retriever, generation = (by_type[k] for k in ("span", "retriever", "generation"))
        tool = by_type.get("tool")
        operations = [retriever, *([tool] if tool else [])]
        assert len(spans) == 2 + len(operations)
        prompt_id = metadata(generation)["prompt_id"]
        prompts.add(prompt_id)
        assert root["spanId"] == trace_root_span_id(trace_id)
        assert root["name"] == CHAT_OPERATION_NAME and generation["name"] == GENERATION_OPERATION_NAME
        assert all(child["parentSpanId"] == root["spanId"] for child in [*operations, generation])
        assert retriever["name"] == REFERENCE_RETRIEVER_NAME
        assert json.loads(attributes(retriever)["langfuse.observation.input"]) == {"source_id": "SRC-01", "prompt_id": prompt_id}
        assert json.loads(attributes(retriever)["langfuse.observation.output"]) == source
        for operation in operations:
            attrs, meta = attributes(operation), metadata(operation)
            assert meta["invocation"] == "application" and meta["simulated"] is True
            assert meta["evidence_kind"] == "authored-synthetic-history"
            assert meta["request_id"] == trace_id and meta["source_id"] == source["id"]
            assert "evaluation_subject" not in meta
            assert not any(key.startswith("langfuse.observation.prompt.") for key in attrs)
            assert not any(key in attrs for key in ("langfuse.observation.model.name",
                "langfuse.observation.usage_details", "langfuse.observation.cost_details"))
        messages = json.loads(attributes(generation)["langfuse.observation.input"])
        model_reference = json.loads(messages[0]["content"].split("\n\nReference context:\n", 1)[1])
        if tool:
            calculations += 1
            assert prompt_id == "PR-02" and metadata(root)["fixture_case_id"] == "PC-02"
            assert tool["name"] == FEE_TOOL_NAME
            result = json.loads(attributes(tool)["langfuse.observation.output"])
            assert result == {"currency": "EUR", "period": "calendar_month", "chargeable_withdrawals": 1, "total_fee": "1.50"}
            assert model_reference["calculation_results"] == metadata(generation)["calculation_results"]
            assert model_reference.pop("calculation_results") == [{"operation": FEE_TOOL_NAME,
                "arguments": json.loads(attributes(tool)["langfuse.observation.input"]), "result": result}]
        assert model_reference == source
        assert messages[1:-1] == metadata(root)["prior_messages"]
        assert messages[-1] == json.loads(attributes(root)["langfuse.observation.input"])
        assert all(message["role"] in {"system", "user", "assistant"} and "tool_calls" not in message for message in messages)
        assert metadata(generation)["reference_context"] == metadata(root)["reference_context"] == source
        for attr in ("langfuse.session.id", "langfuse.user.id", "langfuse.environment"):
            assert len({attributes(span)[attr] for span in spans}) == 1
        start = lambda span: int(span["startTimeUnixNano"])
        end = lambda span: int(span["endTimeUnixNano"])
        assert start(root) <= start(retriever) < end(retriever)
        if tool:
            assert end(retriever) == start(tool) < end(tool)
        assert end(operations[-1]) == start(generation) < end(generation) <= end(root)
    assert calculations == population_plan(24)["fee_calculations"] == 1
    assert prompts == {"PR-01", "PR-02", "PR-03"}


def test_flow_three_distinct_links_and_unprompted_lookup(history):
    flows = defaultdict(list)
    for event in history:
        if "spanId" in event and (metadata(event).get("fixture_case_id") == "FLOW-01" or metadata(event).get("operation_id") == "SIM-LOOKUP"):
            flows[event["traceId"]].append(event)
    assert len(flows) == 4
    for operations in flows.values():
        gens = [e for e in operations if attributes(e)["langfuse.observation.type"] == "generation"]
        tools = [e for e in operations if attributes(e)["langfuse.observation.type"] == "retriever"]
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
        "target_traces": 1620, "generations": 2100, "observations": 5101, "outcomes": 9320,
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
    # Native prompt experiments receive an existing reference; they do not run
    # the app's retrieval pipeline or fabricate model tool-call messages.
    assert Counter(attributes(span)["langfuse.observation.type"] for span in spans.values()) == {"span": 18, "generation": 18}
    for link in links:
        gen = spans[link["observation_id"]]
        assert gen["traceId"] == link["trace_id"]
        assert attributes(gen)["langfuse.environment"] == "experiment"
    for event in events:
        if event.get("type") == "score-create":
            target = metadata(spans[event["body"]["observationId"]])
            assert target["evaluation_subject"] == "assistant_reply"
            definition = next(d for d in score_definitions().values() if d["name"] == event["body"]["name"])
            assert target["rubric_revisions"][definition["id"]] == definition["revision"]
            assert f"{definition['id']}/{definition['revision']}" in event["body"]["comment"]


def test_seed_and_small_replay_are_deterministic():
    first = build_events(7, {"seed": 19}, run_date=ANCHOR)
    assert first == build_events(7, {"seed": 19}, run_date=ANCHOR)
    assert first != build_events(7, {"seed": 20}, run_date=ANCHOR)


@pytest.mark.parametrize("seed", [1, 19, 42, 73])
def test_conditional_operation_plan_matches_selected_history(seed):
    events = build_events(72, {"seed": seed}, run_date=ANCHOR)
    spans = [event for event in events if "spanId" in event]
    plan = population_plan(72, {"seed": seed})
    assert len(spans) == plan["observations"]
    assert sum(span["name"] == FEE_TOOL_NAME for span in spans) == plan["fee_calculations"]
    assert not any(attributes(span)["langfuse.observation.type"] == "agent" for span in spans)
    for span in spans:
        if metadata(span).get("operation_id") == "SIM-LOOKUP":
            assert attributes(span)["langfuse.observation.type"] == "retriever"
            assert span["name"] == REFERENCE_RETRIEVER_NAME
            assert metadata(span)["evidence_kind"] == "authored-synthetic-history"


def test_history_emits_all_factual_categories_without_null_or_numeric_substitution(tmp_path):
    from synth.receipt import make_receipt
    events = finalize(build_events(1620, {'seed': 42}, run_date=ANCHOR))
    factual = [e['body'] for e in events if e.get('type') == 'score-create'
               and e['body']['name'] in ('record_fidelity', 'claim_support')]
    for name in ('record_fidelity', 'claim_support'):
        assert {s['value'] for s in factual if s['name'] == name} == {'Pass', 'Fail', 'Not applicable'}
    assert all(s['dataType'] == 'CATEGORICAL' for s in factual)
    spans = {e['spanId']: e for e in events if 'spanId' in e}
    for score in factual:
        eid = 'E-02' if score['name'] == 'record_fidelity' else 'E-03'
        expected = metadata(spans[score['observationId']])['expected_outcomes'][eid]
        assert expected == {'value': score['value'], 'data_type': 'CATEGORICAL', 'status': 'complete'}
    spool = tmp_path / 'spool.ndjson'
    spool.write_text('offline receipt test')
    receipt = make_receipt(events, spool, run_date=ANCHOR, seed=42, target_traces=1620)
    for name in ('record_fidelity', 'claim_support'):
        assert {s['value'] for t in receipt['representative_traces'] for s in t['scores']
                if s['name'] == name} == {'Pass', 'Fail', 'Not applicable'}


def test_rubric_provenance_is_scoped_to_score_subject_and_trace_prompts(history):
    definitions = score_definitions()
    by_trace = defaultdict(list)
    for event in history:
        if 'spanId' in event:
            by_trace[event['traceId']].append(event)
    for spans in by_trace.values():
        prompt_ids = {metadata(span)['prompt_id'] for span in spans
                      if metadata(span).get('evaluation_subject') == 'assistant_reply'}
        trace_revisions = {eid: definitions[eid]['revision'] for pid in sorted(prompt_ids)
                           for eid in prompt_by_id(pid)['evaluation_ids']}
        for span in spans:
            attrs, meta = attributes(span), metadata(span)
            assert 'rubric_revision' not in meta
            assert json.loads(attrs['langfuse.trace.metadata.rubric_revisions']) == trace_revisions
            subject = meta.get('evaluation_subject')
            if subject:
                expected = {eid: definitions[eid]['revision'] for eid in prompt_by_id(meta['prompt_id'])['evaluation_ids']
                            if definitions[eid]['subject'] == subject}
                assert meta['rubric_revisions'] == expected
                if subject == 'user_input':
                    assert set(expected.values()) == {'r1'}
                if 'E-02' in expected:
                    assert expected['E-02'] == expected['E-03'] == 'r2'
