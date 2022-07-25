from django.core.management import BaseCommand

from dissco.settings.base import BASE_DIR
from maturity.loading import load

DEFAULT_DATA_DIR = BASE_DIR / 'maturity' / 'defs'


class Command(BaseCommand):

    def handle(self, *args, **options):
        load(DEFAULT_DATA_DIR, self.stdout, self.stderr)
