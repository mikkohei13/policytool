from pathlib import Path

from policy.loading.utils import upsert_object, load_yaml
from policy.models import Service, ServiceComponent


def load_services(root: Path):
    if not root.exists():
        return

    for service_def_path in root.iterdir():
        service_def: dict = load_yaml(service_def_path)
        service_component_defs: list[dict] = service_def.pop('components', [])
        service = upsert_object(Service, service_def)
        if service_component_defs:
            load_service_components(service, service_component_defs)


def load_service_components(service: Service, service_component_defs: list[dict]):
    id_start = (service.id * 1000) + 1
    for sc_id, service_component_def in enumerate(service_component_defs, start=id_start):
        upsert_object(ServiceComponent, service_component_def, object_id=sc_id, service=service)
