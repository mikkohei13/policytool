from dataclasses import dataclass
from enum import Enum
from itertools import chain
from pathlib import Path
from typing import TypeVar, Type, Generic

import yaml
from django.db.models import Model


class PolicyLoadError(Exception):
    """
    Generic policy loading error, all errors we can detect will be raised using this
    """
    pass


def load_yaml(path: Path) -> dict | list:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


class UpsertResult(Enum):
    CREATED = 'created'
    UPDATED = 'updated'
    NOOP = 'noop'

    def __str__(self) -> str:
        if self == UpsertResult.NOOP:
            return 'no change'
        return self.value


M = TypeVar('M', bound=Model)


@dataclass
class Result(Generic[M]):
    object: M
    result: UpsertResult

    def __iter__(self):
        yield self.object
        yield self.result


def upsert_object(model: Type[M], definition: dict | None = None, object_id: int | None = None,
                  ignore: set | None = None, **kwargs) -> Result[M]:
    if definition is None:
        definition = {}

    object_id: int = definition.pop('id', object_id)
    if object_id is None:
        raise PolicyLoadError(f'{model.__name__} id must be defined')

    try:
        model_object = model.objects.get(id=object_id)
        result = UpsertResult.UPDATED
    except model.DoesNotExist:
        model_object = model(id=object_id)
        result = UpsertResult.CREATED

    if ignore is None:
        ignore = set()
    changed = False
    for field, value in chain(definition.items(), kwargs.items()):
        if field not in ignore:
            if hasattr(model_object, field):
                current = getattr(model_object, field)
                if current != value:
                    setattr(model_object, field, value)
                    changed = True
            else:
                setattr(model_object, field, value)
                changed = True

    if changed:
        model_object.save()
    else:
        result = UpsertResult.NOOP

    return Result(model_object, result)
