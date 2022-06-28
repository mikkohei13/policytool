from django.core.exceptions import ObjectDoesNotExist

from common.models import Institution
from maturity.models import Category, SubCategory, InstitutionSubCategory
from qa.packs import PackProvider, Answer, Pack, PackSummary, Question, QuestionType, \
    PackDoesNotExist, QuestionDoesNotExist


def to_pack_summary(pack_type: str, institution: Institution, category: Category) -> PackSummary:
    question_count = 0
    answered_count = 0
    for subcategory in category.subcategories.all():
        question_count += 1
        if subcategory.institution_subcategories.filter(institution=institution).exists():
            answered_count += 1

    return PackSummary(p_id=category.id, name=category.name, p_type=pack_type,
                       size=question_count, answered=answered_count,
                       description=category.description)


def to_pack(pack_type: str, institution: Institution, category: Category) -> Pack:
    questions = []
    for subcategory in category.subcategories.all().order_by('order', 'id'):
        questions.append(to_question(institution, subcategory))
    return Pack(p_id=category.id, name=category.name, p_type=pack_type, questions=questions,
                description=category.description)


def to_question(institution: Institution, subcategory: SubCategory) -> Question:
    try:
        institution_subcategory = subcategory.institution_subcategories.get(institution=institution)
        answer = Answer(institution_subcategory.value, institution_subcategory.comment)
    except ObjectDoesNotExist:
        answer = None

    # TODO: right now all questions are required...
    return Question(q_id=subcategory.id, order=subcategory.order, text=subcategory.prompt,
                    q_type=QuestionType.MATURITY, answer=answer, period=subcategory.period)


class DigitalMaturityPackProvider(PackProvider):

    def get_packs(self, institution: Institution) -> list[PackSummary]:
        return [
            to_pack_summary(self.pack_type, institution, category)
            for category in Category.objects.all().order_by('id')
        ]

    def get_pack(self, institution: Institution, pack_id: int) -> Pack:
        try:
            return to_pack(self.pack_type, institution, Category.objects.get(pk=pack_id))
        except ObjectDoesNotExist as e:
            raise PackDoesNotExist() from e

    def save_answer(self, institution: Institution, question_id: int, answer: Answer):
        try:
            subcategory = SubCategory.objects.get(pk=question_id)
        except ObjectDoesNotExist as e:
            raise QuestionDoesNotExist() from e

        if (InstitutionSubCategory.objects.filter(institution=institution, subcategory=subcategory)
                .exists()):
            # this will actually delete all previous answers
            self.delete_answer(institution, question_id)

        # create a new institution subcomponent as an answer
        isub = InstitutionSubCategory(value=int(answer.value), comment=answer.comment,
                                      institution=institution, subcategory=subcategory)
        isub.save()

    def delete_answer(self, institution: Institution, question_id: int):
        try:
            subcategory = SubCategory.objects.get(pk=question_id)
        except ObjectDoesNotExist as e:
            raise QuestionDoesNotExist() from e

        subcategory.institution_subcategories.filter(institution=institution).delete()
