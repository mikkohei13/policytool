from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from django.http import Http404
from django.utils.module_loading import import_string

from common.models import InstitutionUser


class QuestionType(Enum):
    BOOL = 'bool'
    STRING = 'string'
    TEXT = 'text'
    NUMBER = 'number'
    OPTION_SINGLE = 'option'
    OPTION_MULTIPLE = 'options'
    MATURITY = 'maturity'


# TODO: could turn this into an abstract class and use polymorphism for each type?
@dataclass
class Answer:
    value: Any
    comment: str = ''

    def to_dict(self) -> dict[str, Any]:
        return {
            'value': self.value,
            'comment': self.comment,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'Answer':
        value = data.get('value')
        if value is None or value == '':
            raise InvalidAnswer()
        if data.get('comment') is None:
            # django says store empty strings instead of nulls so here we go
            data['comment'] = ''
        return Answer(data['value'], data['comment'])


# TODO: could turn this into an abstract class and use polymorphism for each type?
class Question:

    def __init__(self, q_id: int, text: str, q_type: QuestionType, hint: str = '', order: int = 0,
                 required: bool = True, options: list[str] | None = None,
                 answer: Answer | None = None, **extra):
        self.id = q_id
        self.order = order
        self.text = text
        self.hint = hint
        self.type = q_type
        self.required = required
        self.options = options
        self.answer = answer
        self.extra = extra

    @property
    def answered(self) -> bool:
        return self.answer is not None

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'order': self.order,
            'text': self.text,
            'hint': self.hint,
            'type': self.type.value,
            'required': self.required,
            'options': self.options,
            'answer': self.answer if self.answer is None else self.answer.to_dict(),
            **self.extra,
        }


class PackStatus(Enum):
    COMPLETE = 'complete'
    INCOMPLETE = 'incomplete'
    NOT_STARTED = 'not_started'


def serialise_datetime(dt: datetime | None) -> str | None:
    return dt.isoformat(sep=' ') if dt else None


class PackSummary:

    def __init__(self, p_id: int, name: str, p_type: str, responder_id: int, size: int,
                 answered: int, finished_at: datetime | None, **extra):
        self.id = p_id
        self.name = name
        self.type = p_type
        self.responder_id = responder_id
        self.size = size
        self.answered = answered
        self.finished_at = finished_at
        self.extra = extra

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'responder_id': self.responder_id,
            'size': self.size,
            'answered': self.answered,
            'finished_at': serialise_datetime(self.finished_at),
            **self.extra,
        }


class Pack:

    def __init__(self, p_id: int, name: str, p_type: str, responder_id: int,
                 questions: list[Question], finished_at: datetime | None, **extra):
        self.id = p_id
        self.name = name
        self.type = p_type
        self.responder_id = responder_id
        self.questions = questions
        self.finished_at = finished_at
        self.extra = extra

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'responder_id': self.responder_id,
            'questions': [question.to_dict() for question in self.questions],
            'finished_at': serialise_datetime(self.finished_at),
            **self.extra,
        }


class PackProvider(ABC):

    def __init__(self, pack_type: str):
        self.pack_type = pack_type

    @abstractmethod
    def has_permission(self, user: InstitutionUser, responder_id: int) -> bool:
        ...

    @abstractmethod
    def get_packs(self, responder_id: int) -> list[PackSummary]:
        ...

    @abstractmethod
    def get_pack(self, responder_id: int, pack_id: int) -> Pack:
        ...

    @abstractmethod
    def save_answer(self, responder_id: int, pack_id: int, question_id: int, answer: Answer):
        ...

    @abstractmethod
    def delete_answer(self, responder_id: int, pack_id: int, question_id: int):
        ...

    @abstractmethod
    def finish(self, responder_id: int, pack_id: int, state: bool):
        ...

    @abstractmethod
    def reset_pack(self, responder_id: int, pack_id: int):
        ...


class PackDoesNotExist(Http404):
    pass


class QuestionDoesNotExist(Http404):
    pass


class PackTypeDoesNotExist(Http404):
    pass


class InvalidAnswer(Exception):
    pass


def load_providers(config: dict[str, str] | None) -> dict[str, PackProvider]:
    providers = {}
    if config:
        for pack_type, pack_provider_class in config.items():
            providers[pack_type] = import_string(pack_provider_class)(pack_type)
    return providers
