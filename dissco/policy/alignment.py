from dataclasses import dataclass
from typing import Iterable, Any

from common.models import Institution
from policy.models import InstitutionPolicyComponent, ServicePolicyMapping, PolicyComponentType, \
    Rule, PolicyComponentOption


def join_options(options: Iterable[PolicyComponentOption]) -> str:
    return ' | '.join(option.value for option in options)


@dataclass
class AlignmentResult:
    passed: bool
    mapping: ServicePolicyMapping
    message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            'passed': self.passed,
            'policy_component_name': self.mapping.policy_component.name,
            'message': self.message,
        }


class AlignmentValidatorRegistry:

    def __init__(self):
        self._validators = {}

    def register(self, component_type: PolicyComponentType, rule: Rule):
        def decorator(function):
            self._validators[(component_type, rule)] = function
            return function

        return decorator

    def validate(self, mapping: ServicePolicyMapping,
                 answer: InstitutionPolicyComponent) -> AlignmentResult:
        key = (mapping.policy_component.get_type(), mapping.get_rule())
        try:
            validator = self._validators[key]
            return validator(mapping, answer)
        except KeyError:
            raise Exception(f'No validator for {key} found')


validators = AlignmentValidatorRegistry()


def calculate_alignment(mapping: ServicePolicyMapping, institution: Institution) -> AlignmentResult:
    try:
        answer = InstitutionPolicyComponent.objects.get(policy_component=mapping.policy_component,
                                                        institution=institution)
        return validators.validate(mapping, answer)
    except InstitutionPolicyComponent.DoesNotExist:
        return AlignmentResult(False, mapping, 'No answer provided')


@validators.register(PolicyComponentType.BOOL, Rule.EQUAL)
def validate_bool_equal(mapping: ServicePolicyMapping,
                        answer: InstitutionPolicyComponent) -> AlignmentResult:
    if not answer.value:
        return AlignmentResult(False, mapping, 'No value provided')
    elif mapping.allowed_value == answer.value:
        return AlignmentResult(True, mapping)
    else:
        return AlignmentResult(False, mapping, f'The only valid choice is {mapping.allowed_value}, '
                                               f'you chose {answer.value}')


@validators.register(PolicyComponentType.NUMBER, Rule.EQUAL)
def validate_number_equal(mapping: ServicePolicyMapping,
                          answer: InstitutionPolicyComponent) -> AlignmentResult:
    if not answer.value:
        return AlignmentResult(False, mapping, 'No value provided')
    elif float(mapping.allowed_value) == float(answer.value):
        return AlignmentResult(True, mapping)
    else:
        return AlignmentResult(False, mapping, f'The only valid choice is {mapping.allowed_value}, '
                                               f'you chose {answer.value}')


@validators.register(PolicyComponentType.OPTION_SINGLE, Rule.EQUAL)
def validate_option_single_equal(mapping: ServicePolicyMapping,
                                 answer: InstitutionPolicyComponent) -> AlignmentResult:
    chosen: PolicyComponentOption | None = answer.chosen_options.first()
    allowed: PolicyComponentOption = mapping.allowed_options.first()
    if not chosen:
        return AlignmentResult(False, mapping, 'No choice made')
    elif chosen == allowed:
        return AlignmentResult(True, mapping)
    else:
        return AlignmentResult(False, mapping, 'The only valid choice is '
                                               f'"{mapping.allowed_value}", you chose '
                                               f'"{answer.value}"')


@validators.register(PolicyComponentType.OPTION_SINGLE, Rule.OR)
def validate_option_single_or(mapping: ServicePolicyMapping,
                              answer: InstitutionPolicyComponent) -> AlignmentResult:
    chosen: PolicyComponentOption | None = answer.chosen_options.first()
    allowed: set[PolicyComponentOption] = set(mapping.allowed_options.all())
    if not chosen:
        return AlignmentResult(False, mapping, 'No choice made')
    elif chosen in allowed:
        return AlignmentResult(True, mapping)
    else:
        return AlignmentResult(False, mapping, f'The valid choices are "{join_options(allowed)}", '
                                               f'you chose "{chosen.value}"')


@validators.register(PolicyComponentType.OPTION_MULTIPLE, Rule.EQUAL)
def validate_option_multiple_equal(mapping: ServicePolicyMapping,
                                   answer: InstitutionPolicyComponent) -> AlignmentResult:
    chosen: set[PolicyComponentOption] = set(answer.chosen_options.all())
    allowed: set[PolicyComponentOption] = set(mapping.allowed_options.all())
    if not chosen:
        return AlignmentResult(False, mapping, 'No choice made')
    elif chosen == allowed:
        return AlignmentResult(True, mapping)
    else:
        not_allowed = chosen.difference(allowed)
        return AlignmentResult(False, mapping, f'You must choose exactly "{join_options(allowed)}",'
                                               f' you chose: "{join_options(not_allowed)}"')


@validators.register(PolicyComponentType.OPTION_MULTIPLE, Rule.OR)
def validate_option_multiple_or(mapping: ServicePolicyMapping,
                                answer: InstitutionPolicyComponent) -> AlignmentResult:
    chosen: set[PolicyComponentOption] = set(answer.chosen_options.all())
    allowed: set[PolicyComponentOption] = set(mapping.allowed_options.all())
    if not chosen:
        return AlignmentResult(False, mapping, 'No choice made')
    elif chosen & allowed:
        return AlignmentResult(True, mapping)
    else:
        not_allowed = chosen.difference(allowed)
        return AlignmentResult(False, mapping, 'You must choose at least one of '
                                               f'"{join_options(allowed)}", but you chose '
                                               f'"{join_options(not_allowed)}" which aren not '
                                               'allowed')
