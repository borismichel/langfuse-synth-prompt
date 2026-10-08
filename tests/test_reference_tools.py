from copy import deepcopy
import pytest
from synth.catalog import load_fixture
from synth.reference_tools import reference_arguments, validate_reference


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
