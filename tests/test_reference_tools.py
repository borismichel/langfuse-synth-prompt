from copy import deepcopy
import pytest
from synth.catalog import load_fixture
from synth.reference_tools import reference_arguments, validate_reference, fee_arguments, calculate_fee, generation_reference, withdrawal_count


@pytest.mark.parametrize('pid', ['PR-01', 'PR-02', 'PR-03'])
def test_resolver_preserves_source_facts_without_mutating_catalog(pid):
    source = load_fixture('product')['source']
    result = validate_reference(source, reference_arguments(pid))
    assert result == source
    result['waiver']['exclusions'].clear()
    assert source['waiver']['exclusions']


@pytest.mark.parametrize('mutation', ['missing', 'wrong-source', 'negative-fee', 'boolean-fee', 'missing-exclusion', 'missing-unknowns'])
def test_resolver_rejects_incomplete_or_mismatched_reference(mutation):
    source = deepcopy(load_fixture('product')['source'])
    if mutation == 'missing': del source['action_boundary']
    elif mutation == 'wrong-source': source['id'] = 'wrong'
    elif mutation == 'negative-fee': source['monthly_fee'] = -1
    elif mutation == 'boolean-fee': source['monthly_fee'] = True
    elif mutation == 'missing-exclusion': del source['waiver']['exclusions']
    else: source['unknowns'] = []
    with pytest.raises(ValueError):
        validate_reference(source, reference_arguments('PR-01'))


@pytest.mark.parametrize("count,total,chargeable", [("three", "1.50", 1), ("two", "0.00", 0), ("0", "0.00", 0), ("10", "12.00", 8)])
def test_fee_uses_explicit_count_and_reference_facts(count, total, chargeable):
    source = load_fixture("product")["source"]
    message = f"I made {count} cash withdrawals this calendar month. What withdrawal fee applies?"
    arguments = fee_arguments("PR-02", message, source)
    result = calculate_fee(arguments)
    assert result == {"currency": "EUR", "period": "calendar_month", "chargeable_withdrawals": chargeable, "total_fee": total}
    context = generation_reference(source, arguments, result)
    assert context.pop("calculation_results")[0]["result"] == result
    assert context == source and "calculation_results" not in source
    source["cash_withdrawals"]["fee_each_after_included"] = 0.10
    assert calculate_fee(fee_arguments("PR-02", message, source))["total_fee"] == format(chargeable / 10, ".2f")


@pytest.mark.parametrize("message", [
    "Actually, I made two withdrawals, not three.", "What if I make a third?",
    'Someone said "I made three cash withdrawals this calendar month. What withdrawal fee applies?"',
    "I made three cash withdrawals last calendar month. What withdrawal fee applies?",
    "I made three cash withdrawals this calendar month. What withdrawal fee applies? Or was it two?",
    "I made -3 cash withdrawals this calendar month. What withdrawal fee applies?",
    "I made 1.5 cash withdrawals this calendar month. What withdrawal fee applies?",
    "I receive EUR 1300 salary and withdrew cash.",
])
def test_ambiguous_or_unsupported_inputs_never_create_a_calculation(message):
    assert withdrawal_count("PR-02", message) is None
    assert fee_arguments("PR-02", message, load_fixture("product")["source"]) is None


def test_other_assistants_do_not_invoke_fee_calculator():
    message = "I made three cash withdrawals this calendar month. What withdrawal fee applies?"
    for pid in ("PR-01", "PR-03"):
        assert fee_arguments(pid, message, load_fixture("product")["source"]) is None


@pytest.mark.parametrize("field,value", [("included_per_calendar_month", True), ("included_per_calendar_month", -1),
    ("fee_each_after_included", float("nan")), ("fee_each_after_included", float("inf")),
    ("fee_each_after_included", -1), ("fee_each_after_included", 0.001)])
def test_invalid_calculation_facts_fail_instead_of_inventing_a_fee(field, value):
    source = load_fixture("product")["source"]
    source["cash_withdrawals"][field] = value
    with pytest.raises(ValueError):
        fee_arguments("PR-02", "I made three cash withdrawals this calendar month. What withdrawal fee applies?", source)
