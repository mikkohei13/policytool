from pathlib import Path

from django.core.management.base import OutputWrapper
from django.db import transaction

from policy.loading.mappings import load_mappings
from policy.loading.policies import load_policies
from policy.loading.services import load_services
from policy.loading.utils import UpsertResult, UpsertManager


@transaction.atomic
def load(data_dir: Path, stdout: OutputWrapper, stderr: OutputWrapper):
    upsert_manager = UpsertManager()

    load_services(data_dir / 'services', upsert_manager)
    load_policies(data_dir / 'policies', upsert_manager)
    load_mappings(data_dir / 'mappings', upsert_manager)

    upsert_manager.delete_old()

    stdout.write(f'Load complete:')
    upsert_manager.report(stdout)
