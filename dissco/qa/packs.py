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
    comment: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            'value': self.value,
            'comment': self.comment,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> 'Answer':
        if not data.get('value'):
            raise InvalidAnswer()
        return Answer(data['value'], data.get('comment'))


# TODO: could turn this into an abstract class and use polymorphism for each type?
@dataclass
class Question:
    id: int
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
class Pack(ABC):
    id: int
    name: str
    questions: list[Question]

    @property
    def pack_status(self) -> PackStatus:
        number_of_answers = sum(1 for question in self.questions if question.answered)
        if number_of_answers == len(self.questions):
            return PackStatus.COMPLETE
        elif number_of_answers == 0:
            return PackStatus.NOT_STARTED
        else:
            return PackStatus.INCOMPLETE

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'status': self.pack_status.value,
            'questions': [question.to_dict() for question in self.questions],
        }


class PackProvider(ABC):

    @abstractmethod
    def get_packs(self, institution: Institution) -> list[Pack]:
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
            providers[pack_type] = import_string(pack_provider_class)()
    return providers
