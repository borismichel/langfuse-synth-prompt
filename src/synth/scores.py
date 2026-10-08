"""Categorical factual verdicts; authored 1/0/null labels remain source truth."""
from __future__ import annotations

FACTUAL_CRITERIA = frozenset({'E-02', 'E-03'})
CATEGORIES = ('Pass', 'Fail', 'Not applicable')
SCORE_CONTRACT = 'categorical-factual-r2'


def outcome_value(eid: str, value):
    if eid not in FACTUAL_CRITERIA:
        return value
    if value in CATEGORIES:
        return value
    if value is None:
        return 'Not applicable'
    if isinstance(value, (int, float)) and not isinstance(value, bool) and value in (0, 1):
        return 'Pass' if value == 1 else 'Fail'
    raise ValueError(f'Invalid categorical fixture outcome for {eid}: {value!r}')


def outcome_values(outcomes: dict) -> dict:
    return {eid: outcome_value(eid, value) for eid, value in outcomes.items()}


def read_score_value(score):
    # Core v4.1.1 Score.value prefers numeric_value even on categorical scores.
    # Category codes are nominal and must never be presented as measurements.
    return score.string_value if score.data_type == 'CATEGORICAL' else score.value
