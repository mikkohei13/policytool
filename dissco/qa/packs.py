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
        if not data.get('value'):
            raise InvalidAnswer()
        if data.get('comment') is None:
            # django says store empty strings instead of nulls so here we go
            data['comment'] = ''
        return Answer(data['value'], data['comment'])


# TODO: could turn this into an abstract class and use polymorphism for each type?
@dataclass
class Question:
    id: int
    order: int
    text: str
    hint: str
    type: QuestionType
    required: bool
    options: list[str] | None = None
    answer: Answer | None = None

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
        }


class PackStatus(Enum):
    COMPLETE = 'complete'
    INCOMPLETE = 'incomplete'
    NOT_STARTED = 'not_started'


@dataclass
class PackSummary:
    id: int
    name: str
    type: str
    size: int
    answered: int

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'answered': self.answered,
        }


@dataclass
class Pack:
    id: int
    name: str
    type: str
    questions: list[Question]

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'questions': [question.to_dict() for question in self.questions],
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
    def save_answer(self, institution: Institution, question_id: int, answer: Answer):
        ...

    @abstractmethod
    def delete_answer(self, institution: Institution, question_id: int):
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
