"""Model-free production history assembled exclusively with core event builders.

Catalog calibration assets and v2/v4 experiments are outside production counts.
Only the supplied run_date and seeded substreams determine chronology and IDs.
"""
from __future__ import annotations

from collections import Counter
from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime, time, timedelta, timezone
import json
from typing import Any
from zoneinfo import ZoneInfo

from langfuse_synth_core.rng import Rng
from langfuse_synth_core.seed.events import generation_event, observation_event, score_event, trace_event
from langfuse_synth_core.seed.otlp import trace_root_span_id

from .catalog import dataset_items, load_fixture, prompt_by_id, score_definitions, system_prompt
from .config import DERIVATION_HOOK
from .reference_tools import (REFERENCE_RETRIEVER_NAME, REFERENCE_TOOL_NAME,
                              reference_arguments, validate_reference)

WINDOW_DAYS = 28
HISTORY_TRACES = 1620
HISTORY_COUNTS = {"PR-01": 540, "PR-02": 325, "PR-03": 215, "FLOW-01": 240,
                  "PR-06": 120, "PR-07": 80, "PR-08": 100}
BERLIN = ZoneInfo("Europe/Berlin")
MODEL_RATES = {"demo-compact-v1": (0.4, 1.6), "demo-standard-v1": (1.0, 4.0),
               "demo-reasoning-v1": (2.0, 8.0)}
MODEL_BY_PROMPT = {f"PR-{i:02}": "demo-compact-v1" if i in (4, 5, 7) else
                   "demo-reasoning-v1" if i in (6, 9) else "demo-standard-v1" for i in range(1, 10)}
TOKEN_BASES = {"PR-01": (680, 180), "PR-02": (420, 110), "PR-03": (510, 140),
               "PR-04": (260, 16), "PR-05": (320, 32), "PR-06": (1300, 210),
               "PR-07": (480, 75), "PR-08": (500, 125), "PR-09": (900, 190)}


def _allocate(total: int, weights: Mapping[str, int]) -> dict[str, int]:
    denominator = sum(weights.values())
    counts = {key: total * weight // denominator for key, weight in weights.items()}
    order = sorted(weights, key=lambda key: (-(total * weights[key] % denominator), key))
    for key in order[:total - sum(counts.values())]:
        counts[key] += 1
    return counts


def _session_lengths(turns: int, prompt_id: str) -> list[int]:
    exact = {"PR-01": (72, 72, 36), "PR-02": (43, 43, 22), "PR-03": (29, 29, 14)}
    if turns == HISTORY_COUNTS[prompt_id]:
        a, b, c = exact[prompt_id]
        return [2] * a + [3] * b + [5] * c
    lengths, remaining = [], turns
    while remaining:
        length = min((2, 3, 2, 3, 5)[len(lengths) % 5], remaining)
        if remaining - length == 1 and length < 5:
            length += 1
        lengths.append(length)
        remaining -= length
    return lengths


def population_plan(target_traces: int, params: Mapping[str, Any] | None = None,
                    *, run_date: datetime | None = None) -> dict:
    """Pure volume arithmetic; does not materialize or seed the large population."""
    count = int(DERIVATION_HOOK(target_traces, params or {})["target_traces"])
    if count < 0:
        raise ValueError("target_traces must be nonnegative")
    counts = _allocate(count, HISTORY_COUNTS)
    generations = count + 2 * counts["FLOW-01"]
    outcomes = counts["PR-01"] * 8 + (counts["PR-02"] + counts["PR-03"]) * 7
    outcomes += counts["FLOW-01"] * 3 + counts["PR-06"] + counts["PR-07"] + counts["PR-08"] * 3
    lengths = {pid: _session_lengths(counts[pid], pid) for pid in ("PR-01", "PR-02", "PR-03")}
    sessions = sum(len(values) for values in lengths.values())
    chat_turns = sum(counts[pid] for pid in lengths)
    return {"target_traces": count, "request_counts": counts, "generations": generations,
            "observations": count + generations + counts["FLOW-01"] + 2 * chat_turns, "outcomes": outcomes,
            "chat_turns": chat_turns, "chat_sessions": sessions,
            "chat_users": sessions - 2 * (sessions // 5),
            "session_lengths": {pid: dict(sorted(Counter(values).items())) for pid, values in lengths.items()}}


def local_day_bounds(run_date: datetime, day_offset: int) -> tuple[datetime, datetime]:
    """Convert each local midnight independently, retaining 23/25-hour DST days."""
    if run_date.tzinfo is None:
        raise ValueError("run_date must be timezone-aware")
    date = run_date.astimezone(BERLIN).date() + timedelta(days=day_offset)
    return (datetime.combine(date, time.min, BERLIN).astimezone(timezone.utc),
            datetime.combine(date + timedelta(days=1), time.min, BERLIN).astimezone(timezone.utc))


def _version(prompt_id: str, day: int) -> int:
    for version in prompt_by_id(prompt_id)["versions"]:
        interval = version["relative_days_inclusive"]
        if version["use"] == "production_history" and interval[0] <= day <= interval[1]:
            return version["version"]
    raise ValueError(f"No production version for {prompt_id} on D{day}")


def _session_schedule(count: int, rng: Rng, run_date: datetime) -> list[tuple[datetime, int]]:
    weekday = [d for d in range(-28, 0) if local_day_bounds(run_date, d)[0].astimezone(BERLIN).weekday() < 5]
    weekend = [d for d in range(-28, 0) if d not in weekday]
    weekend_count = round(count * .25)
    def spread(days, n):
        return [days[round(i * (len(days) - 1) / max(1, n - 1)) % len(days)] for i in range(n)]
    choices = spread(weekend, weekend_count) + spread(weekday, count - weekend_count)
    rng.sub("days").shuffle(choices)
    allocations = _allocate(count, {"overnight": 25, "daytime": 40, "evening": 35})
    buckets = [key for key, n in allocations.items() for _ in range(n)]
    rng.sub("hours").shuffle(buckets)
    result = []
    for i, (day, bucket) in enumerate(zip(choices, buckets)):
        r = rng.sub("arrival", i)
        # Reserve the final hour for longer five-turn resumptions, still in this day.
        low, high = {"overnight": (0, 9), "daytime": (9, 17), "evening": (17, 23)}[bucket]
        start, _ = local_day_bounds(run_date, day)
        local = start.astimezone(BERLIN).replace(hour=r.randint(low, high - 1), minute=r.randint(0, 29), second=r.randint(0, 59))
        result.append((local.astimezone(timezone.utc), day))
    return result


def _task_timestamp(index: int, rng: Rng, run_date: datetime) -> tuple[datetime, int]:
    days = [d for d in range(-28, 0) if local_day_bounds(run_date, d)[0].astimezone(BERLIN).weekday() < 5]
    day = -1 if index == 0 else days[(index - 1) % len(days)]
    local = local_day_bounds(run_date, day)[0].astimezone(BERLIN).replace(
        hour=rng.randint(9, 17), minute=rng.randint(0, 59), second=rng.randint(0, 59))
    return local.astimezone(timezone.utc), day


def _root(*, trace_id, timestamp, name, metadata, user_id=None, session_id=None, input=None, output=None,
          environment="production-history", obs_type="agent"):
    # Compose core builders: shell propagation and observation-local evaluator context.
    # Putting evaluation_subject into trace metadata would leak it to every child.
    shell = trace_event(trace_id=trace_id, timestamp=timestamp, name=name, user_id=user_id,
                        session_id=session_id, tags=["authored-history", "fictional"],
                        environment=environment, input=input, output=output)
    root = observation_event(obs_id=trace_root_span_id(trace_id), trace_id=trace_id,
                             name=name, obs_type=obs_type, start=timestamp,
                             environment=environment, metadata={**metadata, "request_id": trace_id}, input=input, output=output)
    attrs = {a["key"]: a for a in shell["attributes"]}
    attrs.update({a["key"]: a for a in root["attributes"]})
    shell["attributes"] = list(attrs.values())
    return shell


def _reference_resolution(rng, trace_id, index, prompt_id, start, source):
    """Authored timing for the application's local read-and-validate operation.

    The app invokes this tool before calling the provider; it is not a model
    tool-call message. An isolated substream preserves existing session choices.
    """
    arguments = reference_arguments(prompt_id)
    resolved = validate_reference(source, arguments)
    tool_id = rng.obs_id("reference-tool", index)
    retrieval_start = start + timedelta(milliseconds=5)
    retrieval_end = retrieval_start + timedelta(milliseconds=rng.sub("reference-timing", index).randint(25, 55))
    end = retrieval_end + timedelta(milliseconds=8)
    metadata = {"application_id": prompt_by_id(prompt_id)["application_id"],
                "request_id": trace_id, "source_id": arguments["source_id"],
                "cohort": "production-history", "evidence_kind": "authored-synthetic-history",
                "invocation": "application", "simulated": True}
    tool = observation_event(obs_id=tool_id, trace_id=trace_id,
        name=REFERENCE_TOOL_NAME, obs_type="tool", parent_id=trace_root_span_id(trace_id),
        start=start, end=end, environment="production-history",
        input=arguments, output=resolved, metadata=metadata)
    retriever = observation_event(obs_id=rng.obs_id("reference-retriever", index), trace_id=trace_id,
        name=REFERENCE_RETRIEVER_NAME, obs_type="retriever", parent_id=tool_id,
        start=retrieval_start, end=retrieval_end, environment="production-history",
        input={"source_id": arguments["source_id"]}, output=source, metadata=metadata)
    return [tool, retriever], end, resolved


def _metadata(prompt_id, version, case_id, source, question, history, *, subject, output=None):
    prompt = prompt_by_id(prompt_id)
    result = {"application_id": prompt["application_id"], "prompt_id": prompt_id,
              "prompt_name": prompt["name"], "resolved_version": version, "fixture_case_id": case_id,
              "cohort": "production-history", "evidence_kind": "authored-synthetic-history",
              "evaluation_subject": subject, "current_user_message": question,
              "prior_messages": deepcopy(history), "reference_context": deepcopy(source),
              "rubric_revision": "r1", "judge_executed": False}
    if output is not None:
        result["assistant_reply"] = output
    return result


def _generation(rng, trace_id, index, prompt_id, version, start, case_id, question, source, history, output, outcomes,
                environment="production-history"):
    prompt = prompt_by_id(prompt_id)
    obs_id = rng.obs_id("generation", index, prompt_id)
    base_in, base_out = TOKEN_BASES[prompt_id]
    r = rng.sub("accounting", index, prompt_id)
    in_tokens = base_in + (7 - version) * 20 + r.randint(-20, 20) + len(history) * 18
    out_tokens = max(8, base_out + (7 - version) * 10 + r.randint(-8, 8))
    model = MODEL_BY_PROMPT[prompt_id]
    rate_in, rate_out = MODEL_RATES[model]
    in_cost, out_cost = in_tokens * rate_in / 1_000_000, out_tokens * rate_out / 1_000_000
    end = start + timedelta(milliseconds=850 + (7 - version) * 70 + r.randint(0, 450))
    metadata = _metadata(prompt_id, version, case_id, source, question, history,
                         subject="assistant_reply", output=output)
    metadata["cohort"] = environment
    metadata["request_id"] = trace_id
    definitions = score_definitions()
    metadata.update({"synthetic_pricing": True, "synthetic_usage": True,
                     "expected_outcomes": {eid: {"value": value, "status": "inapplicable" if value is None else "complete"}
                                           for eid, value in sorted(outcomes.items())
                                           if definitions[eid]["subject"] == "assistant_reply"}})
    rendered = output if isinstance(output, str) else json.dumps(output, sort_keys=True)
    generation = generation_event(obs_id=obs_id, trace_id=trace_id, name=prompt["name"],
        parent_id=trace_root_span_id(trace_id), start=start, end=end, environment=environment,
        model=model, model_parameters={"temperature": 0, "fixture_replay": True},
        usage_details={"input": in_tokens, "output": out_tokens, "total": in_tokens + out_tokens},
        cost_details={"input": in_cost, "output": out_cost, "total": in_cost + out_cost},
        prompt_name=prompt["name"], prompt_version=version,
        input=[{"role": "system", "content": system_prompt(prompt_id, version) +
               "\n\nReference context:\n" + json.dumps(source, sort_keys=True)},
               *deepcopy(history), {"role": "user", "content": question}],
        output={"role": "assistant", "content": rendered}, metadata=metadata)
    return generation, end, obs_id


def _scores(rng, trace_id, index, root_id, gen_id, outcomes, timestamp, case_id,
            environment="production-history"):
    definitions, result = score_definitions(), []
    for eid, value in sorted(outcomes.items()):
        # Numeric score records require numbers. Null stays explicit on its subject.
        if value is None:
            continue
        definition = definitions[eid]
        subject = root_id if definition["subject"] == "user_input" else gen_id
        detail = "quoted" if eid == "E-07" and (case_id == "C-07" or "quoted" in case_id) else "direct"
        result.append(score_event(score_id=rng.score_id(index, eid, subject), name=definition["name"],
            value=value, data_type="NUMERIC", trace_id=trace_id, observation_id=subject,
            timestamp=timestamp + timedelta(milliseconds=20), environment=environment,
            comment=f"Authored fixture expectation; no judge executed. {eid}/r1; case {case_id}; "
                    f"subject {definition['subject']}. " + (f"Profanity presence: {detail}. " if eid == "E-07" and value else "") +
                    definition["rubric"]))
    return result


def _historical_reply(turn, prompt_id, version):
    """Deliberate early-version errors, never a claim about executed judge results."""
    output, outcomes = turn["assistant_reply"], dict(turn["expected_scores"])
    if prompt_id == "PR-01" and version in (1, 3) and turn["case_id"] == "C-04":
        output = "Your EUR 1300 transfer meets the EUR 1200 threshold, so the monthly fee is waived."
        outcomes.update({"E-02": 0, "E-03": 0})
    if prompt_id == "PR-02" and version == 1 and turn["case_id"] == "PC-02":
        output = "Three withdrawals cost EUR 4.50 in total."
        outcomes.update({"E-02": 0, "E-03": 0})
    if prompt_id == "PR-03" and version == 1 and turn["case_id"] == "PC-03":
        output = "Yes, a five-month-old proof of address is fine."
        outcomes.update({"E-02": 0, "E-03": 0})
    return output, outcomes


def build_events(target_traces: int, params: Mapping[str, Any], *, run_date: datetime) -> list[dict]:
    """Generate history only; no provider, judge, clock, network or external writes."""
    plan = population_plan(target_traces, params)
    rng = Rng(int(params.get("seed", 42)))
    local_day_bounds(run_date, -1)
    events, counts = [], plan["request_counts"]
    source = load_fixture("product")["source"]
    sessions = []
    for prompt_id in ("PR-01", "PR-02", "PR-03"):
        lengths = _session_lengths(counts[prompt_id], prompt_id)
        rng.sub("lengths", prompt_id).shuffle(lengths)
        sessions.extend((prompt_id, length) for length in lengths)
    schedule = _session_schedule(len(sessions), rng, run_date)
    triples = len(sessions) // 5
    single_users = len(sessions) - 3 * triples
    users = list(range(single_users)) + [single_users + i for i in range(triples) for _ in range(3)]
    rng.sub("users").shuffle(users)
    templates_by_prompt = load_fixture("conversations")
    prompt_session_indices = Counter()
    definitions = score_definitions()
    for session_index, ((prompt_id, length), (start, day), user_index) in enumerate(zip(sessions, schedule, users)):
        r = rng.sub("session", session_index)
        session_id = "history-" + rng.item_id("session", session_index)
        user_id = "fictional-user-" + rng.item_id("user", user_index)
        templates = templates_by_prompt[prompt_id]
        ordinal = prompt_session_indices[prompt_id]
        prompt_session_indices[prompt_id] += 1
        template = r.choices(templates, [t["weight"] for t in templates])[0]
        if ordinal == 0:
            template = templates[0]
        history, timestamp = [], start
        for turn_index in range(length):
            turn = template["turns"][turn_index]
            trace_id = r.trace_id("turn", turn_index)
            version = _version(prompt_id, day)
            output, outcomes = _historical_reply(turn, prompt_id, version)
            metadata = _metadata(prompt_id, version, turn["case_id"], source, turn["user_message"], history, subject="user_input")
            metadata.update({"session_turn": turn_index + 1, "session_length": length, "topic": template["theme"],
                             "relative_day": day, "expected_outcomes": {eid: {"value": value, "status": "complete"}
                                 for eid, value in sorted(outcomes.items()) if definitions[eid]["subject"] == "user_input"}})
            events.append(_root(trace_id=trace_id, timestamp=timestamp, name=prompt_by_id(prompt_id)["title"] + " request",
                user_id=user_id, session_id=session_id, metadata=metadata, obs_type="span",
                input={"role": "user", "content": turn["user_message"]}, output={"role": "assistant", "content": output}))
            reference_events, generation_start, resolved = _reference_resolution(
                r, trace_id, turn_index, prompt_id, timestamp, source)
            events.extend(reference_events)
            gen, end, gen_id = _generation(r, trace_id, turn_index, prompt_id, version, generation_start,
                turn["case_id"], turn["user_message"], resolved, history, output, outcomes)
            events.append(gen)
            events.extend(_scores(r, trace_id, turn_index, trace_root_span_id(trace_id), gen_id, outcomes, end, turn["case_id"]))
            history += [{"role": "user", "content": turn["user_message"]}, {"role": "assistant", "content": output}]
            gap = r.randint(300, 1200) if r.chance(.08) else r.randint(15, 120)
            timestamp = end + timedelta(seconds=gap)
    for index in range(counts["FLOW-01"]):
        r = rng.sub("flow", index)
        start, day = _task_timestamp(index, r, run_date)
        trace_id = r.trace_id(index)
        request = load_fixture("portfolio")["multi_prompt_example"]["user_request"]
        final = dataset_items("PR-09")[0]["expected_output"]
        events.append(_root(trace_id=trace_id, timestamp=start, name="Service request review", metadata={
            "application_id": "APP-04", "fixture_case_id": "FLOW-01", "cohort": "production-history",
            "evidence_kind": "authored-synthetic-history", "relative_day": day},
            input={"role": "user", "content": request}, output={"role": "assistant", "content": final}))
        cursor = start
        for operation, pid in enumerate(("PR-04", "PR-05", "PR-09")):
            if operation == 2:
                tool_end = cursor + timedelta(milliseconds=75)
                events.append(observation_event(obs_id=r.obs_id("lookup"), trace_id=trace_id,
                    name="Reference lookup", obs_type="tool", parent_id=trace_root_span_id(trace_id),
                    start=cursor, end=tool_end, environment="production-history",
                    input={"query": "monthly fee waiver own-account transfer"}, output=source,
                    metadata={"operation_id": "SIM-LOOKUP", "simulated": True, "source_id": "SRC-01"}))
                cursor = tool_end
            case = dataset_items(pid)[0]
            context = case["input"]["reference_context"]
            if pid == "PR-05":
                context = {"required_constraints": ["own-account transfer", "monthly fee waiver"]}
            output = {"intent": "fees"} if pid == "PR-04" else "monthly fee waiver own-account transfer" if pid == "PR-05" else final
            expected = case["metadata"]["expected_scores"]
            gen, end, gen_id = _generation(r, trace_id, operation, pid, _version(pid, day), cursor,
                "FLOW-01", request, context, [], output, expected)
            events.append(gen)
            events.extend(_scores(r, trace_id, operation, trace_root_span_id(trace_id), gen_id, expected, end, "FLOW-01"))
            cursor = end + timedelta(milliseconds=10)
    for pid in ("PR-06", "PR-07", "PR-08"):
        items = dataset_items(pid)
        for index in range(counts[pid]):
            r = rng.sub("task", pid, index)
            start, day = _task_timestamp(index, r, run_date)
            trace_id = r.trace_id(index)
            item = items[index % len(items)]
            question, context = item["input"]["user_message"], item["input"]["reference_context"]
            output, expected = item["expected_output"], item["metadata"]["expected_scores"]
            events.append(_root(trace_id=trace_id, timestamp=start, name=prompt_by_id(pid)["title"] + " request",
                metadata={"application_id": prompt_by_id(pid)["application_id"], "fixture_case_id": item["case_id"],
                          "cohort": "production-history", "relative_day": day, "evidence_kind": "authored-synthetic-history"},
                input={"role": "user", "content": question}, output=output))
            gen, end, gen_id = _generation(r, trace_id, index, pid, _version(pid, day), start,
                item["case_id"], question, context, [], output, expected)
            events.append(gen)
            events.extend(_scores(r, trace_id, index, trace_root_span_id(trace_id), gen_id, expected, end, item["case_id"]))
    return events


def build_historical_experiment_events(params: Mapping[str, Any], *, run_date: datetime) -> tuple[list[dict], list[dict]]:
    """Eighteen fixed authored v2/v4 records for native historical dataset runs.

    These are synthetic replay, not completed paid model/judge executions. The
    caller provisions assets and attaches the returned links after ingestion.
    Like native prompt-only experiments, they consume the dataset's supplied
    reference context and do not run the application's reference tool pipeline.
    """
    from .catalog import historical_experiment_cases

    rng = Rng(int(params.get("seed", 42))).sub("historical-experiments")
    definitions, events, links = score_definitions(), [], []
    for index, item in enumerate(historical_experiment_cases()):
        pid, version = item["prompt_id"], item["prompt_version"]
        prompt = prompt_by_id(pid)
        day = next(v for v in prompt["versions"] if v["version"] == version)["relative_days_inclusive"][0]
        timestamp = local_day_bounds(run_date, day)[0] + timedelta(hours=12, minutes=index)
        r = rng.sub("case", index)
        trace_id = r.trace_id(index)
        question, source = item["input"]["user_message"], item["input"]["reference_context"]
        history, output = item["input"]["conversation_history"], item["expected_output"]
        outcomes = {eid: value for eid, value in item["metadata"]["expected_scores"].items()
                    if definitions[eid]["subject"] == "assistant_reply"}
        events.append(_root(trace_id=trace_id, timestamp=timestamp,
            name=prompt["title"] + " historical experiment", environment="experiment",
            metadata={"application_id": prompt["application_id"], "cohort": "experiment",
                      "fixture_case_id": item["case_id"], "execution_kind": "authored-historical-experiment",
                      "judge_executed": False}, input={"role": "user", "content": question}, output=output))
        gen, end, gen_id = _generation(r, trace_id, index, pid, version, timestamp, item["case_id"],
                                       question, source, history, output, outcomes, environment="experiment")
        events.append(gen)
        events.extend(_scores(r, trace_id, index, trace_root_span_id(trace_id), gen_id, outcomes,
                              end, item["case_id"], environment="experiment"))
        links.append({"prompt_id": pid, "version": version, "case_id": item["case_id"],
                      "trace_id": trace_id, "observation_id": gen_id,
                      "run_name": f"authored-history-{pid}-v{version}-r1"})
    return events, links
