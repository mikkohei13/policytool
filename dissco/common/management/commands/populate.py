import requests
from django.core.management.base import BaseCommand

from common.models import Institution

GBIF_REGISTRY_API_URL = 'https://registry-api.gbif.org/grscicoll/institution?code={}'
MISSING_ROR_ID = ''


def extract_ror_id(data: dict, default: str = MISSING_ROR_ID) -> str:
    """
    Given a data dict from the GBIF Registry API, extract the ROR ID, if there is one. If a ROR is
    not found, the passed default value is returned.

    :param data: the GBIF Registry API data
    :param default: the default value to return if a ROR is not found (defaults to the empty string)
    :returns: the ROR ID or the default parameter
    """
    return next(
        (alt['code'] for alt in data.get('alternativeCodes', []) if alt['description'] == 'ROR'),
        default
    )


# TODO: get a list of DiSSCo institutions from an API
class Command(BaseCommand):
    help = 'Updates the database with the data about the given institutions. Existing institution' \
           'objects are updated if matched using their code, otherwise new objects are created.'

    def add_arguments(self, parser):
        parser.add_argument('codes', nargs='+', type=str)

    def handle(self, *args, **options):
        codes = options['codes']
        for i, code in enumerate(codes, start=1):
            r = requests.get(GBIF_REGISTRY_API_URL.format(code))
            result = r.json()
            count = result['count']
            if count != 1:
                self.stdout.write(self.style.ERROR(f'Found {count} institutions matching {code}, '
                                                   f'wanted to find 1'))
            else:
                try:
                    institution = Institution.objects.get(code=code)
                except Institution.DoesNotExist:
                    institution = Institution()

                data = result['results'][0]
                institution.name = data['name']
                institution.code = data['code']
                institution.ror_id = extract_ror_id(data)
                institution.save()
                self.stdout.write(self.style.SUCCESS(f'Updated {code} [{i}/{len(codes)}]'))
