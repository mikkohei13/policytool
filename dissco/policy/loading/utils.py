from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import TypeVar, Type

import yaml
from django.db.models import Model


class PolicyLoadError(Exception):
    """
    Generic policy loading error, all errors we can detect will be raised using this
    """
    pass


def load_yaml(path: Path) -> dict | list:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


@dataclass
class PolicyLoadSummary:
    created: int = 0
    updated: int = 0
    nooped: int = 0

    def reset(self):
        self.created = 0
        self.updated = 0
        self.nooped = 0

    def update(self):
        self.updated += 1

    def create(self):
        self.created += 1

    def noop(self):
        self.nooped += 1


M = TypeVar('M', bound=Model)


def upsert_object(model: Type[M], definition: dict | None = None, object_id: int | None = None,
                  ignore: set | None = None, **kwargs) -> M:
    if definition is None:
        definition = {}

    object_id: int = definition.pop('id', object_id)
    if object_id is None:
        raise PolicyLoadError(f'{model.__name__} id must be defined')

    try:
        model_object = model.objects.get(id=object_id)
    except model.DoesNotExist:
        model_object = model(id=object_id)

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
    return model_object
