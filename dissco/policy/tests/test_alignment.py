from dataclasses import dataclass
from functools import partial
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


@dataclass
class Scenario:
    type: PolicyComponentType
    rule: Rule
    allowed: list[str]
    choices: list[str]
    ok: bool
    options: tuple[str] = ('a', 'b', 'c', 'd', 'e', 'f')
    prefix: str = str(uuid4())

    def create_mapping(self) -> ServicePolicyMapping:
        service = Service(name=f'{self.prefix}_service')
        service.save()

        service_component = ServiceComponent(name=f'{self.prefix}_service_component',
                                             service=service)
        service_component.save()

        policy_category = PolicyCategory(name=f'{self.prefix}_policy_category')
        policy_category.save()

        policy_area = PolicyArea(name=f'{self.prefix}_policy_area', number=1,
                                 category=policy_category)
        policy_area.save()

        policy_component = PolicyComponent(name=f'{self.prefix}_policy_component', type=self.type,
                                           question=f'{self.prefix}_question',
                                           policy_area=policy_area)
        policy_component.save()

        allowed_options = []
        for value in self.options:
            option = PolicyComponentOption(value=value, policy_component=policy_component)
            if value in self.allowed:
                allowed_options.append(option)
            option.save()
            policy_component.options.add(option)
        policy_component.save()

        mapping = ServicePolicyMapping(rule=self.rule, service_component=service_component,
                                       policy_component=policy_component)
        mapping.save()

        mapping.allowed_options.set(allowed_options)
        mapping.save()
        return mapping

    def create_institution(self) -> Institution:
        institution = Institution(name=f'{self.prefix}_test_institution')
        institution.save()
        return institution


OptionSingleEqual = partial(Scenario, type=PolicyComponentType.OPTION_SINGLE, rule=Rule.EQUAL)
OptionSingleOr = partial(Scenario, type=PolicyComponentType.OPTION_SINGLE, rule=Rule.OR)
OptionMultipleEqual = partial(Scenario, type=PolicyComponentType.OPTION_MULTIPLE, rule=Rule.EQUAL)
OptionMultipleOr = partial(Scenario, type=PolicyComponentType.OPTION_MULTIPLE, rule=Rule.OR)

scenarios = [
    # no answer
    OptionSingleEqual(allowed=['a'], choices=[], ok=False),
    # valid answer
    OptionSingleEqual(allowed=['a'], choices=['a'], ok=True),
    # invalid answer
    OptionSingleEqual(allowed=['a'], choices=['b'], ok=False),

    # no answer
    OptionSingleOr(allowed=['a', 'c'], choices=[], ok=False),
    # valid answer
    OptionSingleOr(allowed=['a', 'c'], choices=['a'], ok=True),
    # another valid answer
    OptionSingleOr(allowed=['a', 'c'], choices=['c'], ok=True),
    # invalid answer
    OptionSingleOr(allowed=['a', 'c'], choices=['b'], ok=False),

    # no answer
    OptionMultipleEqual(allowed=['a', 'c'], choices=[], ok=False),
    # valid answer
    OptionMultipleEqual(allowed=['a', 'c'], choices=['a', 'c'], ok=True),
    # invalid answer (just wrong)
    OptionMultipleEqual(allowed=['a', 'c'], choices=['d'], ok=False),
    # invalid answer (partially just wrong)
    OptionMultipleEqual(allowed=['a', 'c'], choices=['a', 'd'], ok=False),
    # invalid answer (subset is right)
    OptionMultipleEqual(allowed=['a', 'c'], choices=['a', 'b', 'c'], ok=False),

    # no answer
    OptionMultipleOr(allowed=['a', 'c'], choices=[], ok=False),
    # valid answer (full match)
    OptionMultipleOr(allowed=['a', 'c'], choices=['a', 'c'], ok=True),
    # valid answer (partial match)
    OptionMultipleOr(allowed=['a', 'c'], choices=['c'], ok=True),
    # valid answer (partial match + mismatch)
    OptionMultipleOr(allowed=['a', 'c'], choices=['a', 'b', 'c'], ok=True),
    # invalid answer
    OptionMultipleOr(allowed=['a', 'c'], choices=['d'], ok=False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('scenario', scenarios)
def test_option_scenarios(scenario: Scenario):
    mapping = scenario.create_mapping()

    answer = InstitutionPolicyComponent(institution=scenario.create_institution(),
                                        policy_component=mapping.policy_component)
    answer.save()
    answer.chosen_options.set([option for option in mapping.policy_component.options.all()
                               if option.value in scenario.choices])
    answer.save()

    result = validators.validate(mapping, answer)
    assert result.passed == scenario.ok
