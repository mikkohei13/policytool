from uuid import uuid4

import pytest

from common.models import Institution
from policy.alignment import validators
from policy.models import ServicePolicyMapping, InstitutionPolicyComponent, PolicyComponent, \
    PolicyComponentType, Rule, ServiceComponent, PolicyComponentOption, Service, PolicyArea, \
    PolicyCategory

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
    policy_component = PolicyComponent(type=PolicyComponentType.BOOL)
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
    policy_component = PolicyComponent(type=PolicyComponentType.NUMBER)
    mapping = ServicePolicyMapping(allowed_value=allowed_value, policy_component=policy_component,
                                   rule=Rule.EQUAL)
    answer = InstitutionPolicyComponent(value=answer_value)
    result = validators.validate(mapping, answer)
    assert result.passed == ok


def create_mapping(options: list[str], allowed: list[str], component_type: PolicyComponentType,
                   rule: Rule) -> ServicePolicyMapping:
    def random_str() -> str:
        return str(uuid4())

    service = Service(name=random_str())
    service.save()

    service_component = ServiceComponent(name=random_str(), service=service)
    service_component.save()

    policy_category = PolicyCategory(name=random_str())
    policy_category.save()

    policy_area = PolicyArea(name=random_str(), number=1, category=policy_category)
    policy_area.save()

    policy_component = PolicyComponent(type=component_type, policy_area=policy_area)
    policy_component.save()

    allowed_options = []
    for value in options:
        option = PolicyComponentOption(value=value, policy_component=policy_component)
        if value in allowed:
            allowed_options.append(option)
        option.save()
        policy_component.options.add(option)
    policy_component.save()

    mapping = ServicePolicyMapping(rule=rule, service_component=service_component,
                                   policy_component=policy_component)
    mapping.save()

    mapping.allowed_options.set(allowed_options)
    mapping.save()
    return mapping


@pytest.mark.django_db
class TestOptionSingleEqual:

    def test_no_choice(self):
        mapping = create_mapping(['a', 'b', 'c', 'd'], ['b'],
                                 PolicyComponentType.OPTION_SINGLE, Rule.EQUAL)

        institution = Institution(name='test institution')
        institution.save()
        answer = InstitutionPolicyComponent(institution=institution,
                                            policy_component=mapping.policy_component)
        answer.save()
        result = validators.validate(mapping, answer)
        assert not result.passed

    def test_valid_choice(self):
        mapping = create_mapping(['a', 'b', 'c', 'd'], ['b'],
                                 PolicyComponentType.OPTION_SINGLE, Rule.EQUAL)

        institution = Institution(name='test institution')
        institution.save()
        answer = InstitutionPolicyComponent(institution=institution,
                                            policy_component=mapping.policy_component)
        answer.save()
        answer.chosen_options.add(mapping.policy_component.options.all()[1])
        answer.save()
        result = validators.validate(mapping, answer)
        assert result.passed

    def test_invalid_choice(self):
        mapping = create_mapping(['a', 'b', 'c', 'd'], ['b'],
                                 PolicyComponentType.OPTION_SINGLE, Rule.EQUAL)

        institution = Institution(name='test institution')
        institution.save()
        answer = InstitutionPolicyComponent(institution=institution,
                                            policy_component=mapping.policy_component)
        answer.save()
        answer.chosen_options.add(mapping.policy_component.options.all()[0])
        answer.save()
        result = validators.validate(mapping, answer)
        assert not result.passed


option_single_equal_scenarios = [
    # no answer
    (['a', 'b'], ['a'], '', False),
    # a valid answer
    (['a', 'b'], ['a'], 'a', True),
    # an invalid answer
    (['a', 'b'], ['a'], 'b', False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('options, allowed_options, choice, ok', option_single_equal_scenarios)
def test_option_single_equal(options: list[str], allowed_options: list[str], choice: str, ok: bool):
    mapping = create_mapping(options, allowed_options, PolicyComponentType.OPTION_SINGLE,
                             Rule.EQUAL)
    institution = Institution(name='test institution')
    institution.save()
    answer = InstitutionPolicyComponent(institution=institution,
                                        policy_component=mapping.policy_component)
    answer.save()
    answer.chosen_options.set([option for option in mapping.policy_component.options.all()
                               if option.value == choice])
    answer.save()

    result = validators.validate(mapping, answer)
    assert result.passed == ok


option_single_equal_scenarios = [
    # no answer
    (['a', 'b'], ['a'], '', False),
    # a valid answer
    (['a', 'b'], ['a'], 'a', True),
    # an invalid answer
    (['a', 'b'], ['a'], 'b', False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('options, allowed_options, choice, ok', option_single_equal_scenarios)
def test_option_single_equal(options: list[str], allowed_options: list[str], choice: str, ok: bool):
    mapping = create_mapping(options, allowed_options, PolicyComponentType.OPTION_SINGLE,
                             Rule.EQUAL)
    institution = Institution(name='test institution')
    institution.save()
    answer = InstitutionPolicyComponent(institution=institution,
                                        policy_component=mapping.policy_component)
    answer.save()
    answer.chosen_options.set([option for option in mapping.policy_component.options.all()
                               if option.value == choice])
    answer.save()

    result = validators.validate(mapping, answer)
    assert result.passed == ok


option_single_or_scenarios = [
    # no answer
    (['a', 'b'], ['a'], '', False),
    # a valid answer
    (['a', 'b', 'c', 'd'], ['a', 'c'], 'c', True),
    # an invalid answer
    (['a', 'b'], ['a', 'd'], 'b', False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('options, allowed_options, choice, ok', option_single_or_scenarios)
def test_option_single_or(options: list[str], allowed_options: list[str], choice: str, ok: bool):
    mapping = create_mapping(options, allowed_options, PolicyComponentType.OPTION_SINGLE,
                             Rule.OR)
    institution = Institution(name='test institution')
    institution.save()
    answer = InstitutionPolicyComponent(institution=institution,
                                        policy_component=mapping.policy_component)
    answer.save()
    answer.chosen_options.set([option for option in mapping.policy_component.options.all()
                               if option.value == choice])
    answer.save()

    result = validators.validate(mapping, answer)
    assert result.passed == ok


option_multiple_equal_scenarios = [
    # no answer
    (['a', 'b'], ['a'], [], False),
    # a valid answer
    (['a', 'b', 'c', 'd'], ['a', 'c'], ['a', 'c'], True),
    # an invalid answer (mismatch)
    (['a', 'b', 'c', 'd'], ['a', 'c'], ['a', 'b'], False),
    # an invalid answer (subset + mismatch)
    (['a', 'b', 'c', 'd'], ['a', 'c'], ['a', 'b', 'c'], False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('options, allowed_options, choices, ok', option_multiple_equal_scenarios)
def test_option_multiple_equal(options: list[str], allowed_options: list[str], choices: list[str],
                               ok: bool):
    mapping = create_mapping(options, allowed_options, PolicyComponentType.OPTION_MULTIPLE,
                             Rule.EQUAL)
    institution = Institution(name='test institution')
    institution.save()
    answer = InstitutionPolicyComponent(institution=institution,
                                        policy_component=mapping.policy_component)
    answer.save()
    answer.chosen_options.set([option for option in mapping.policy_component.options.all()
                               if option.value in choices])
    answer.save()

    result = validators.validate(mapping, answer)
    assert result.passed == ok


option_multiple_or_scenarios = [
    # no answer
    (['a', 'b'], ['a'], [], False),
    # a valid answer (full match)
    (['a', 'b', 'c', 'd'], ['a', 'c'], ['a', 'c'], True),
    # a valid answer (partial match)
    (['a', 'b', 'c', 'd'], ['a', 'c'], ['c'], True),
    # a valid answer (partial + mismatch)
    (['a', 'b', 'c', 'd'], ['a', 'c'], ['a', 'b', 'c'], True),
    # an invalid answer (mismatch)
    (['a', 'b', 'c', 'd'], ['a', 'c'], ['b'], False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('options, allowed_options, choices, ok', option_multiple_or_scenarios)
def test_option_multiple_or(options: list[str], allowed_options: list[str], choices: list[str],
                            ok: bool):
    mapping = create_mapping(options, allowed_options, PolicyComponentType.OPTION_MULTIPLE,
                             Rule.OR)
    institution = Institution(name='test institution')
    institution.save()
    answer = InstitutionPolicyComponent(institution=institution,
                                        policy_component=mapping.policy_component)
    answer.save()
    answer.chosen_options.set([option for option in mapping.policy_component.options.all()
                               if option.value in choices])
    answer.save()

    result = validators.validate(mapping, answer)
    assert result.passed == ok
