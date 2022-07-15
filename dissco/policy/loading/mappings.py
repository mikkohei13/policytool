from itertools import count
from pathlib import Path

from policy.loading.utils import load_yaml, PolicyLoadError, gen_offset_id, UpsertResult, \
    UpsertManager
from policy.models import Service, ServiceComponent, PolicyComponent, ServicePolicyMapping, \
    PolicyComponentOption


def find_policy_component(policy_area_id: int, ref: int) -> PolicyComponent:
    component_id = gen_offset_id(policy_area_id, ref)
    return PolicyComponent.objects.get(id=component_id)


def find_service_component(service_id: int, ref: int) -> ServiceComponent:
    component_id = gen_offset_id(service_id, ref)
    return ServiceComponent.objects.get(id=component_id)


def find_policy_component_options(policy_component: PolicyComponent,
                                  refs: list[int]) -> list[PolicyComponentOption]:
    ids = [gen_offset_id(policy_component.id, ref) for ref in refs]
    return list(PolicyComponentOption.objects.filter(id__in=ids))


def load_mappings(root: Path, upsert_manager: UpsertManager):
    if not root.exists():
        return

    offset_counter = count(start=1)

    for mapping_path in root.iterdir():
        mapping_def = load_yaml(mapping_path)

        # ensure the service we're mapping into exists
        service_id = mapping_def['service']
        if not Service.objects.filter(id=service_id).exists():
            raise PolicyLoadError(f"Couldn't find service {service_id} in {mapping_path}")

        for sc_mappings_def in mapping_def['mappings']:
            # find the service component with the given ref
            service_component = find_service_component(service_id,
                                                       sc_mappings_def['service_component'])

            for mapping_def in sc_mappings_def['policy_components']:
                policy_component = find_policy_component(mapping_def.pop('area'),
                                                         mapping_def.pop('ref'))
                option_values = mapping_def.pop('options', [])
                # if the policy component is option based but the user has defined a single allowed
                # option as the value, move it over. This is technically an error on the user's
                # part, but we can account for it easily enough
                if policy_component.is_option_based() and 'value' in mapping_def:
                    option_values = [mapping_def.pop('value')]

                if 'value' in mapping_def:
                    # convert the value to a string as that's all we store in the db
                    mapping_def['allowed_value'] = str(mapping_def.pop('value'))

                mapping_id = next(offset_counter)
                mapping = upsert_manager.upsert(ServicePolicyMapping, mapping_def,
                                                object_id=mapping_id,
                                                service_component=service_component,
                                                policy_component=policy_component)

                if policy_component.is_option_based() and option_values:
                    existing_options = set(mapping.allowed_options.all())
                    options = set(find_policy_component_options(policy_component, option_values))
                    mapping.allowed_options.set(options)
                    mapping.save()

                    upsert_manager.add(UpsertResult.DELETED, len(existing_options - options))
                    upsert_manager.add(UpsertResult.NOOP, len(existing_options & options))
                    upsert_manager.add(UpsertResult.CREATED, len(options - existing_options))
