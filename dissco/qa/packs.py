from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any

from django.utils.module_loading import import_string

from common.models import Institution


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


class PackSummary:

    def __init__(self, p_id: int, name: str, p_type: str, size: int, answered: int, **extra):
        self.id = p_id
        self.name = name
        self.type = p_type
        self.size = size
        self.answered = answered
        self.extra = extra

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'answered': self.answered,
            **self.extra,
        }


class Pack:

    def __init__(self, p_id: int, name: str, p_type: str, questions: list[Question], **extra):
        self.id = p_id
        self.name = name
        self.type = p_type
        self.questions = questions
        self.extra = extra

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'questions': [question.to_dict() for question in self.questions],
            **self.extra,
        }


class PackProvider(ABC):

    def __init__(self, pack_type: str):
        self.pack_type = pack_type

    @abstractmethod
    def get_packs(self, institution: Institution) -> list[PackSummary]:
        ...

    @abstractmethod
    def get_pack(self, institution: Institution, pack_id: int) -> Pack:
        ...

    @abstractmethod
    def save_answer(self, institution: Institution, pack_id: int, question_id: int, answer: Answer):
        ...

    @abstractmethod
    def delete_answer(self, institution: Institution, pack_id: int, question_id: int):
        pass


class PackDoesNotExist(Exception):
    pass


class QuestionDoesNotExist(Exception):
    pass


class PackTypeDoesNotExist(Exception):
    pass


class InvalidAnswer(Exception):
    pass


def load_providers(config: dict[str, str] | None) -> dict[str, PackProvider]:
    providers = {}
    if config:
        for pack_type, pack_provider_class in config.items():
            providers[pack_type] = import_string(pack_provider_class)(pack_type)
    return providers
