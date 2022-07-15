from pathlib import Path

from policy.loading.utils import load_yaml, gen_offset_id, UpsertManager
from policy.models import Service, ServiceComponent


def load_services(root: Path, upsert_manager: UpsertManager):
    """
    Load the services from the service definition files.
    """
    if not root.exists():
        return

    for service_def_path in root.iterdir():
        service_def = load_yaml(service_def_path)
        service = upsert_manager.upsert(Service, service_def, ignore={'components'})
        if 'components' in service_def:
            load_service_components(service, service_def['components'], upsert_manager)


def load_service_components(service: Service, defs: list[dict], upsert_manager: UpsertManager):
    """
    Load the service components from the service definition.
    """
    for service_component_def in defs:
        component_id = gen_offset_id(service.id, service_component_def.pop('ref'))
        upsert_manager.upsert(ServiceComponent, service_component_def, object_id=component_id,
                              service=service)
