from pathlib import Path

from policy.loading.utils import upsert_object, load_yaml
from policy.models import Service, ServiceComponent


def load_services(root: Path):
    """
    Load the services from the service definition files.
    """
    if not root.exists():
        return

    for service_def_path in root.iterdir():
        service_def = load_yaml(service_def_path)
        service, result = upsert_object(Service, service_def, ignore={'components'})
        yield result
        if 'components' in service_def:
            yield from load_service_components(service, service_def['components'])


def load_service_components(service: Service, defs: list[dict]):
    """
    Load the service components from the service definition.
    """
    id_start = (service.id * 1000) + 1
    for component_id, service_component_def in enumerate(defs, start=id_start):
        result = upsert_object(ServiceComponent, service_component_def, object_id=component_id,
                               service=service)
        yield result.result
