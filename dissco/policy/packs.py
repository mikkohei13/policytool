from django.core.exceptions import ObjectDoesNotExist

from common.models import Institution
from policy.models import PolicyArea, PolicyComponent, PolicyComponentOption, \
    InstitutionPolicyComponent, PolicyComponentOptionType
from qa.packs import PackProvider, Pack, Answer, Question, PackDoesNotExist, QuestionDoesNotExist, \
    QuestionType, PackSummary

option_mapping: dict[PolicyComponentOptionType, QuestionType] = {
    PolicyComponentOptionType.BOOL: QuestionType.BOOL,
    PolicyComponentOptionType.NUMBER: QuestionType.NUMBER,
    PolicyComponentOptionType.OPTION_SINGLE: QuestionType.OPTION_SINGLE,
    PolicyComponentOptionType.OPTION_MULTIPLE: QuestionType.OPTION_MULTIPLE,
}


def to_pack_summary(pack_type: str, institution: Institution, policy_area: PolicyArea) \
        -> PackSummary:
    question_count = 0
    answered_count = 0
    for policy_component in policy_area.components.all():
        question_count += 1
        if policy_component.institution_policy_components.filter(institution=institution).exists():
            answered_count += 1

    return PackSummary(p_id=policy_area.id, name=policy_area.name, p_type=pack_type,
                       size=question_count, answered=answered_count, **get_pack_extras(policy_area))


def to_pack(pack_type: str, institution: Institution, policy_area: PolicyArea) -> Pack:
    questions = []
    for policy_component in policy_area.components.all().order_by('order', 'id'):
        questions.append(to_question(institution, policy_component))
    return Pack(p_id=policy_area.id, name=policy_area.name, p_type=pack_type,
                questions=questions, **get_pack_extras(policy_area))


def get_pack_extras(policy_area: PolicyArea) -> dict:
    return {
        'scope': policy_area.scope,
        'category': {
            'name': policy_area.category.name,
            'scope': policy_area.category.scope,
        },
    }


def to_question(institution: Institution, policy_component: PolicyComponent) -> Question:
    # TODO: do we want to include the id as well as the value for each option?
    options = [option.value for option in policy_component.options.all().order_by('value')]
    if not options:
        options = None

    try:
        institutional_policy_component = policy_component.institution_policy_components \
            .get(institution=institution)
        answer = to_answer(policy_component, institutional_policy_component)
    except ObjectDoesNotExist:
        answer = None

    # TODO: could use the presence of a mapping entity to determine if a question is required?
    return Question(q_id=policy_component.id, order=policy_component.order,
                    text=policy_component.question, hint=policy_component.description,
                    q_type=option_mapping[policy_component.get_type()], options=options,
                    answer=answer)


def to_answer(policy_component: PolicyComponent,
              institution_policy_component: InstitutionPolicyComponent) -> Answer:
    if policy_component.is_option_based():
        choices = [choice.value for choice in institution_policy_component.chosen_options.all()]
        return Answer(choices, institution_policy_component.comment)
    else:
        return Answer(institution_policy_component.value, institution_policy_component.comment)


class PolicyPackProvider(PackProvider):
    """
    Mapping:
        - Pack -> PolicyArea
        - Question -> PolicyComponent (question) + PolicyComponentOption (options)
        - Answer -> InstitutionPolicyComponent (answer) + PolicyComponentOption (choices)
    """

    def get_packs(self, institution: Institution) -> list[PackSummary]:
        return [
            to_pack_summary(self.pack_type, institution, policy_area)
            for policy_area in PolicyArea.objects.all().order_by('id')
        ]

    def get_pack(self, institution: Institution, pack_id: int) -> Pack:
        try:
            return to_pack(self.pack_type, institution, PolicyArea.objects.get(pk=pack_id))
        except ObjectDoesNotExist as e:
            raise PackDoesNotExist() from e

    def save_answer(self, institution: Institution, pack_id: int, question_id: int, answer: Answer):
        try:
            policy_component = PolicyComponent.objects.get(pk=question_id)
        except ObjectDoesNotExist as e:
            raise QuestionDoesNotExist() from e

        if (InstitutionPolicyComponent.objects
                .filter(institution=institution, policy_component=policy_component).exists()):
            # this will actually delete all previous answers
            self.delete_answer(institution, pack_id, question_id)

        # create a new institution policy component as an answer
        ipc = InstitutionPolicyComponent(comment=answer.comment, institution=institution,
                                         policy_component=policy_component)
        if policy_component.is_option_based():
            choices = PolicyComponentOption.objects.filter(policy_component=policy_component,
                                                           value__in=answer.value)
            # have to save to be able to add choices
            ipc.save()
            ipc.chosen_options.add(*choices)
        else:
            ipc.value = answer.value
        ipc.save()

    def delete_answer(self, institution: Institution, pack_id: int, question_id: int):
        try:
            policy_component = PolicyComponent.objects.get(pk=question_id)
        except ObjectDoesNotExist as e:
            raise QuestionDoesNotExist() from e

        policy_component.institution_policy_components \
            .filter(institution=institution) \
            .delete()
