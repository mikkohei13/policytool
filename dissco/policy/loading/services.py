from pathlib import Path

from policy.loading.utils import upsert_object, load_yaml, gen_offset_id, UpsertResult
from policy.models import Service, ServiceComponent


def load_services(root: Path):
    """
    Load the services from the service definition files.
    """
    if not root.exists():
        return

    ids = set()

    for service_def_path in root.iterdir():
        service_def = load_yaml(service_def_path)
        service, result = upsert_object(Service, service_def, ignore={'components'})
        yield result
        ids.add(service.id)
        if 'components' in service_def:
            yield from load_service_components(service, service_def['components'])

    deleted, _ = Service.objects.exclude(id__in=ids).delete()
    yield from [UpsertResult.DELETED] * deleted


def load_service_components(service: Service, defs: list[dict]):
    """
    Load the service components from the service definition.
    """
    for service_component_def in defs:
        component_id = gen_offset_id(service.id, service_component_def.pop('ref'))
        result = upsert_object(ServiceComponent, service_component_def, object_id=component_id,
                               service=service)
        yield result.result
