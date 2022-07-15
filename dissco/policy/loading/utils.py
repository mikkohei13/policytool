from collections import defaultdict, Counter
from enum import Enum
from itertools import chain
from pathlib import Path
from typing import TypeVar, Type

import yaml
from django.core.management.base import OutputWrapper
from django.db.models import Model


class PolicyLoadError(Exception):
    """
    Generic policy loading error, all errors we can detect will be raised using this
    """
    pass


def load_yaml(path: Path) -> dict | list:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def gen_offset_id(parent_id: int, child_id: int) -> int:
    return (parent_id * 1000) + child_id


class UpsertResult(Enum):
    CREATED = 'created'
    UPDATED = 'updated'
    NOOP = 'noop'
    DELETED = 'deleted'

    def __str__(self) -> str:
        if self == UpsertResult.NOOP:
            return 'no change'
        return self.value


M = TypeVar('M', bound=Model)


class UpsertManager:

    def __init__(self):
        self._stats = Counter()
        self._seen = defaultdict(set)

    def add(self, result: UpsertResult, count: int = 1):
        if count:
            self._stats[result] += count

    def upsert(self, model: Type[M], definition: dict | None = None, object_id: int | None = None,
               ignore: set | None = None, **kwargs) -> M:
        if definition is None:
            definition = {}

        object_id: int = definition.pop('id', object_id)
        if object_id is None:
            raise PolicyLoadError(f'{model.__name__} id must be defined')

        self._seen[model].add(object_id)

        try:
            model_object = model.objects.get(id=object_id)
            result = UpsertResult.UPDATED
        except model.DoesNotExist:
            model_object = model(id=object_id)
            result = UpsertResult.CREATED

        if ignore is None:
            ignore = set()
        changed = False
        # TODO: need to handle unsetting of attributes
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

        self.add(result)
        return model_object

    def delete_old(self):
        for model, seen_ids in self._seen.items():
            deleted, _ = model.objects.exclude(id__in=seen_ids).delete()
            self.add(UpsertResult.DELETED, deleted)

    def report(self, stdout: OutputWrapper):
        for result, count in self._stats.most_common():
            stdout.write(f'\t{str(result).capitalize()}: {count}')
