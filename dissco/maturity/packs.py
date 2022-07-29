from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from common.models import InstitutionUser
from maturity.models import Category, Question as MaturityQuestion, Answer as MaturityAnswer, \
    Responder, Response
from qa.packs import PackProvider, Answer, Pack, PackSummary, Question, QuestionType, \
    PackDoesNotExist, QuestionDoesNotExist


def get_finished_datetime(responder: Responder, category: Category) -> datetime | None:
    try:
        response = Response.objects.get(responder=responder, category=category)
        return response.finished_at
    except ObjectDoesNotExist:
        return None


def to_pack_summary(pack_type: str, responder: Responder, category: Category) -> PackSummary:
    question_count = 0
    answered_count = 0
    for question in category.questions.all():
        question_count += 1
        if question.answers.filter(responder=responder).exists():
            answered_count += 1

    finished_at = get_finished_datetime(responder, category)

    return PackSummary(p_id=category.id, name=category.name, p_type=pack_type,
                       responder_id=responder.id, size=question_count, answered=answered_count,
                       description=category.description, finished_at=finished_at)


def to_pack(pack_type: str, responder: Responder, category: Category) -> Pack:
    questions = []
    for question in category.questions.all().order_by('order', 'id'):
        questions.append(to_question(responder, question))

    finished_at = get_finished_datetime(responder, category)

    return Pack(p_id=category.id, name=category.name, p_type=pack_type, responder_id=responder.id,
                questions=questions, description=category.description, finished_at=finished_at)


def to_question(responder: Responder, question: MaturityQuestion) -> Question:
    try:
        db_answer = question.answers.get(responder=responder)
        answer = Answer(db_answer.value, db_answer.comment)
    except ObjectDoesNotExist:
        answer = None

    # TODO: right now all questions are required...
    return Question(q_id=question.id, order=question.order, text=question.prompt,
                    q_type=QuestionType.MATURITY, answer=answer, period=question.period)


class DigitalMaturityPackProvider(PackProvider):

    def has_permission(self, institutional_user: InstitutionUser, responder_id: int) -> bool:
        responder = Responder.objects.get(id=responder_id)
        return responder.owner == institutional_user.user

    def get_packs(self, responder_id: int) -> list[PackSummary]:
        responder = Responder.objects.get(id=responder_id)
        return [
            to_pack_summary(self.pack_type, responder, category)
            for category in Category.objects.all().order_by('id')
        ]

    def get_pack(self, responder_id: int, pack_id: int) -> Pack:
        responder = Responder.objects.get(id=responder_id)
        try:
            return to_pack(self.pack_type, responder, Category.objects.get(pk=pack_id))
        except ObjectDoesNotExist as e:
            raise PackDoesNotExist() from e

    def save_answer(self, responder_id: int, pack_id: int, question_id: int, answer: Answer):
        responder: Responder = Responder.objects.get(id=responder_id)
        try:
            question = MaturityQuestion.objects.get(pk=question_id)
        except ObjectDoesNotExist as e:
            raise QuestionDoesNotExist() from e

        if MaturityAnswer.objects.filter(responder=responder, question=question).exists():
            self.delete_answer(responder_id, pack_id, question_id)

        db_answer = MaturityAnswer(value=int(answer.value), comment=answer.comment,
                                   responder=responder, question=question)
        db_answer.save()

    def delete_answer(self, responder_id: int, pack_id: int, question_id: int):
        responder = Responder.objects.get(id=responder_id)
        try:
            question = MaturityQuestion.objects.get(pk=question_id)
        except ObjectDoesNotExist as e:
            raise QuestionDoesNotExist() from e

        question.answers.filter(responder=responder).delete()

    def finish(self, responder_id: int, pack_id: int, state: bool):
        responder = Responder.objects.get(id=responder_id)
        category = Category.objects.get(pk=pack_id)
        try:
            response = Response.objects.get(responder=responder, category=category)
        except ObjectDoesNotExist as e:
            response = Response(responder=responder, category=category)

        response.finished_at = timezone.now() if state else None
        response.save()

    def reset_pack(self, responder_id: int, pack_id: int):
        category = Category.objects.get(pk=pack_id)

        self.finish(responder_id, pack_id, False)

        for question in category.questions.all():
            self.delete_answer(responder_id, pack_id, question.id)
