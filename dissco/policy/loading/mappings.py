from pathlib import Path

from policy.loading.utils import load_yaml, PolicyLoadError, upsert_object
from policy.models import Service, ServiceComponent, PolicyComponent, ServicePolicyMapping, \
    PolicyComponentOption


def find_policy_component(name: str) -> PolicyComponent:
    return PolicyComponent.objects.get(name=name)


def find_service_component(name: str) -> ServiceComponent:
    return ServiceComponent.objects.get(name=name)


def load_mappings(root: Path):
    if not root.exists():
        return

    for mapping_path in root.iterdir():
        mapping_def = load_yaml(mapping_path)

        # ensure the service we're mapping into exists
        service_id = mapping_def['service']
        if not Service.objects.filter(id=service_id).exists():
            raise PolicyLoadError(f"Couldn't find service {service_id} in {mapping_path}")

        for sc_mappings_def in mapping_def['mappings']:
            # find the service component with the given name
            service_component = find_service_component(sc_mappings_def['service_component'])

            id_start = (service_component.id * 1000) + 1
            for mapping_id, mapping_def in enumerate(sc_mappings_def['policy_components'],
                                                     start=id_start):
                policy_component = find_policy_component(mapping_def.pop('name'))
                options = mapping_def.pop('options', [])
                # if the policy component is option based but the user has defined a single allowed
                # option as the value, move it over. This is technically an error on the user's
                # part, but we can account for it easily enough
                if policy_component.is_option_based() and 'value' in mapping_def:
                    options = [mapping_def.pop('value')]

                if 'value' in mapping_def:
                    # convert the value to a string as that's all we store in the db
                    mapping_def['allowed_value'] = str(mapping_def.pop('value'))

                mapping, result = upsert_object(ServicePolicyMapping, mapping_def,
                                                object_id=mapping_id,
                                                service_component=service_component,
                                                policy_component=policy_component)
                yield result

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
