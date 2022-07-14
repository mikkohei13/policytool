from pathlib import Path

from django.db import transaction

from policy.loading.mappings import load_mappings
from policy.loading.policies import load_policies
from policy.loading.services import load_services


@transaction.atomic
def load(data_dir: Path):
    load_services(data_dir / 'services')
    load_policies(data_dir / 'policies')
    load_mappings(data_dir / 'mappings')
