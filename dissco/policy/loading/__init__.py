from collections import Counter
from pathlib import Path

from django.core.management.base import OutputWrapper
from django.db import transaction

from policy.loading.mappings import load_mappings
from policy.loading.policies import load_policies
from policy.loading.services import load_services
from policy.loading.utils import UpsertResult


@transaction.atomic
def load(data_dir: Path, stdout: OutputWrapper, stderr: OutputWrapper):
    tasks = [
        (load_services, 'services'),
        (load_policies, 'policies'),
        (load_mappings, 'mappings'),
    ]
    counter = Counter()
    for func, path in tasks:
        for result in func(data_dir / path):
            counter[result] += 1

    stdout.write(f'Load complete:')
    for result, count in counter.most_common():
        stdout.write(f'\t{str(result).capitalize()}: {count}')
