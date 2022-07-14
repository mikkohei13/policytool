from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import TypeVar, Type

import yaml
from django.db import transaction
from django.db.models import Model

from dissco.settings.base import BASE_DIR
from policy.models import Service, ServiceComponent, PolicyCategory, PolicyArea, PolicyComponent, \
    PolicyComponentOption, ServicePolicyMapping

DEFAULT_DATA_DIR = BASE_DIR / 'policy' / 'data'


# generic policy loading error, all errors we can detect will be raised using this
class PolicyLoadError(Exception):
    pass


def load_yaml(path: Path) -> dict | list:
    return yaml.safe_load(path.read_text(encoding='utf-8'))


def find_policy_component(name: str) -> PolicyComponent | None:
    try:
        return PolicyComponent.objects.get(name=name)
    except PolicyComponent.DoesNotExist:
        return None


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


class PolicyLoader:

    def __init__(self, data_dir: Path = DEFAULT_DATA_DIR):
        self.data_dir = data_dir
        self.summary = PolicyLoadSummary()

    @transaction.atomic
    def load(self) -> PolicyLoadSummary:
        self.load_services()
        self.load_policies()
        self.load_mappings()
        return self.summary

    def _upsert_object(self, model: Type[M], definition: dict | None = None,
                       object_id: int | None = None, ignore: set | None = None, **kwargs) -> M:
        if definition is None:
            definition = {}

        object_id: int = definition.pop('id', object_id)
        if object_id is None:
            raise PolicyLoadError(f'{model.__name__} id must be defined')

        created = False
        try:
            model_object = model.objects.get(id=object_id)
        except model.DoesNotExist:
            model_object = model(id=object_id)
            created = True

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
            if created:
                self.summary.create()
            else:
                self.summary.update()
                print(f'{model}: {model_object.id}')
            model_object.save()
        else:
            self.summary.noop()
        return model_object

    def load_services(self):
        services_dir = self.data_dir / 'services'
        if not services_dir.exists():
            return

        for service_def_path in services_dir.iterdir():
            service_def: dict = load_yaml(service_def_path)
            service_component_defs: list[dict] = service_def.pop('components', [])
            service = self._upsert_object(Service, service_def)
            if service_component_defs:
                self.load_service_components(service, service_component_defs)

    def load_service_components(self, service: Service, service_component_defs: list[dict]):
        id_start = (service.id * 1000) + 1
        for sc_id, service_component_def in enumerate(service_component_defs, start=id_start):
            self._upsert_object(ServiceComponent, service_component_def, object_id=sc_id,
                                service=service)

    def load_policies(self):
        policies_dir = self.data_dir / 'policies'
        if not policies_dir.exists():
            return

        category_defs_path = policies_dir / 'categories.yml'
        if category_defs_path.exists():
            category_defs: list[dict] = load_yaml(category_defs_path)
            for category_def in category_defs:
                self._upsert_object(PolicyCategory, category_def)

        for policy_def_path in policies_dir.iterdir():
            if policy_def_path == category_defs_path:
                continue

            policy_def: dict = load_yaml(policy_def_path)
            policy_component_defs: list[dict] = policy_def.pop('components', [])
            category_id = policy_def.pop('category')
            category = PolicyCategory.objects.get(id=category_id)
            policy_area = self._upsert_object(PolicyArea, policy_def, category=category)
            if policy_component_defs:
                self.load_policy_components(policy_area, policy_component_defs)

    def load_policy_components(self, policy_area: PolicyArea, policy_component_defs: list[dict]):
        id_start = (policy_area.id * 1000) + 1
        for pc_id, policy_component_def in enumerate(policy_component_defs, start=id_start):
            options = policy_component_def.pop('options', [])
            policy_component = self._upsert_object(PolicyComponent, policy_component_def,
                                                   object_id=pc_id, policy_area=policy_area)
            if policy_component_def['type'] == 'options' and options:
                self.load_policy_component_options(policy_component, options)

    def load_policy_component_options(self, policy_component: PolicyComponent, options: list[str]):
        option_id_start = (policy_component.id * 1000) + 1
        for pco_id, option_def in enumerate(options, start=option_id_start):
            self._upsert_object(PolicyComponentOption, object_id=pco_id, value=option_def,
                                policy_component=policy_component)

    def load_mappings(self):
        mappings_dir = self.data_dir / 'mappings'
        if not mappings_dir.exists():
            return

        for mapping_path in mappings_dir.iterdir():
            mapping_def = load_yaml(mapping_path)
            service_id = mapping_def['service']
            if not Service.objects.filter(id=service_id).exists():
                raise PolicyLoadError(f"Couldn't find service {service_id} in {mapping_path}")

            for sc_mappings_def in mapping_def['mappings']:
                service_component = ServiceComponent.objects.get(
                    name=sc_mappings_def['service_component'])
                id_start = (service_component.id * 1000) + 1
                for mapping_id, mapping_def in enumerate(sc_mappings_def['policy_components'],
                                                         start=id_start):
                    pc_name = mapping_def.pop('name')
                    policy_component = find_policy_component(pc_name)
                    if policy_component is None:
                        raise PolicyLoadError(f"Couldn't find policy component named "
                                              f"'{pc_name}' in {mapping_path}")
                    options = mapping_def.pop('options', [])
                    if policy_component.is_option_based() and 'value' in mapping_def:
                        options = [mapping_def.pop('value')]

                    if 'value' in mapping_def:
                        mapping_def['allowed_value'] = str(mapping_def.pop('value'))

                    mapping = self._upsert_object(ServicePolicyMapping, mapping_def,
                                                  object_id=mapping_id,
                                                  service_component=service_component,
                                                  policy_component=policy_component)
                    if policy_component.is_option_based() and options:
                        for value in options:
                            try:
                                option = policy_component.options.get(value=value)
                            except PolicyComponentOption.DoesNotExist:
                                raise PolicyLoadError(f"Couldn't find option '{value}' under "
                                                      f"'{policy_component.name}' in "
                                                      f"{mapping_path}")
                            mapping.allowed_options.add(option)
                        mapping.save()
