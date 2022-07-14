from itertools import count
from pathlib import Path

from policy.loading.utils import load_yaml, PolicyLoadError, upsert_object, gen_offset_id, \
    UpsertResult
from policy.models import Service, ServiceComponent, PolicyComponent, ServicePolicyMapping, \
    PolicyComponentOption


def find_policy_component(policy_area_id: int, ref: int) -> PolicyComponent:
    component_id = gen_offset_id(policy_area_id, ref)
    return PolicyComponent.objects.get(id=component_id)


def find_service_component(service_id: int, ref: int) -> ServiceComponent:
    component_id = gen_offset_id(service_id, ref)
    return ServiceComponent.objects.get(id=component_id)


def find_policy_component_option(policy_component: PolicyComponent,
                                 ref: int) -> PolicyComponentOption:
    option_id = gen_offset_id(policy_component.id, ref)
    return PolicyComponentOption.objects.get(id=option_id)


def load_mappings(root: Path):
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
                options = mapping_def.pop('options', [])
                # if the policy component is option based but the user has defined a single allowed
                # option as the value, move it over. This is technically an error on the user's
                # part, but we can account for it easily enough
                if policy_component.is_option_based() and 'value' in mapping_def:
                    options = [mapping_def.pop('value')]

                if 'value' in mapping_def:
                    # convert the value to a string as that's all we store in the db
                    mapping_def['allowed_value'] = str(mapping_def.pop('value'))

                mapping_id = next(offset_counter)
                mapping, result = upsert_object(ServicePolicyMapping, mapping_def,
                                                object_id=mapping_id,
                                                service_component=service_component,
                                                policy_component=policy_component)
                yield result

                if policy_component.is_option_based() and options:
                    existing_options = mapping.allowed_options.all()
                    for value in options:
                        option = find_policy_component_option(policy_component, value)
                        if option not in existing_options:
                            mapping.allowed_options.add(option)
                            yield UpsertResult.UPDATED
                        else:
                            yield UpsertResult.NOOP
                    mapping.save()
