import pytest

from policy.alignment import validators
from policy.models import ServicePolicyMapping, InstitutionPolicyComponent, PolicyComponent, \
    PolicyComponentOptionType, Rule

bool_equal_scenarios = [
    ('yes', 'yes', True),
    ('yes', 'no', False),
    ('yes', 'notSpecified', False),
    ('yes', 'banana', False),
    ('no', 'no', True),
    ('no', 'notSpecified', False),
    ('no', 'yes', False),
    ('yes', '', False),
    ('no', '', False),
    ('notSpecified', '', False),
]


@pytest.mark.parametrize('allowed_value, answer_value, ok', bool_equal_scenarios)
def test_bool_equal(allowed_value: str, answer_value: str, ok: bool):
    policy_component = PolicyComponent(type=PolicyComponentOptionType.BOOL)
    mapping = ServicePolicyMapping(allowed_value=allowed_value, policy_component=policy_component,
                                   rule=Rule.EQUAL)
    answer = InstitutionPolicyComponent(value=answer_value)
    result = validators.validate(mapping, answer)
    assert result.passed == ok


number_equal_scenarios = [
    ('4', '4', True),
    ('3.1', '3.1', True),
    ('21', '20', False),
    ('10', '10', True),
    ('0', '0', True),
    ('-1.2', '-1.2', True),
    ('5', '-5', False),
    ('2', '', False),
]


@pytest.mark.parametrize('allowed_value, answer_value, ok', number_equal_scenarios)
def test_number_equal(allowed_value: str, answer_value: str, ok: bool):
    policy_component = PolicyComponent(type=PolicyComponentOptionType.NUMBER)
    mapping = ServicePolicyMapping(allowed_value=allowed_value, policy_component=policy_component,
                                   rule=Rule.EQUAL)
    answer = InstitutionPolicyComponent(value=answer_value)
    result = validators.validate(mapping, answer)
    assert result.passed == ok
