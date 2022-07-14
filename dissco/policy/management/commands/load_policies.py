from django.core.management import BaseCommand

from policy.loader import PolicyLoader


class Command(BaseCommand):

    def handle(self, *args, **options):
        loader = PolicyLoader()
        summary = loader.load()
        self.stdout.write(f'Summary: created {summary.created}, updated {summary.updated}, '
                          f'no ops: {summary.nooped}')
