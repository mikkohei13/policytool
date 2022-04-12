from typing import Optional

import pytest
import responses

from common.management.commands.populate import extract_ror_id, Command, GBIF_REGISTRY_API_URL, \
    MISSING_ROR_ID
from common.models import Institution


def test_extract_ror_id_empty():
    assert extract_ror_id({}) == MISSING_ROR_ID


def test_extract_ror_id_missing_ror():
    data = {'alternativeCodes': [{'code': 'abcd', 'description': 'not ROR'}]}
    assert extract_ror_id(data) == MISSING_ROR_ID


def test_extract_ror_id_has_ror():
    ror_id = '039zvsn29'
    data = {'alternativeCodes': [{'code': ror_id, 'description': 'ROR'}]}
    assert extract_ror_id(data) == ror_id


def create_gbif_data(name: str, code: str, ror_id: Optional[str] = None) -> dict:
    data = {
        'name': name,
        'code': code,
        'alternativeCodes': []
    }
    if ror_id:
        data['alternativeCodes'].append({'code': ror_id, 'description': 'ROR'})
    return data


class TestPopulateCommand:

    @responses.activate
    @pytest.mark.django_db
    def test_single_new(self):
        command = Command()
        name = 'Natural History Museum, London'
        code = 'NHMUK'
        ror_id = '039zvsn29'
        mock_result = {
            'count': 1,
            'results': [create_gbif_data(name, code, ror_id)]
        }
        responses.add(responses.GET,
                      'https://registry-api.gbif.org/grscicoll/institution?code=NHMUK',
                      json=mock_result)

        command.handle(codes=('NHMUK',))

        assert Institution.objects.count() == 1
        institution = Institution.objects.get(code='NHMUK')
        assert institution.name == name
        assert institution.code == code
        assert institution.ror_id == ror_id

    @responses.activate
    @pytest.mark.django_db
    def test_single_update(self):
        command = Command()
        name = 'Natural History Museum, London'
        code = 'NHMUK'
        ror_id = '039zvsn29'
        Institution(name=name, code=code, ror_id='a different ROR ID').save()
        mock_result = {
            'count': 1,
            'results': [create_gbif_data(name, code, ror_id)]
        }
        responses.add(responses.GET,
                      'https://registry-api.gbif.org/grscicoll/institution?code=NHMUK',
                      json=mock_result)

        command.handle(codes=('NHMUK',))

        assert Institution.objects.count() == 1
        institution = Institution.objects.get(code='NHMUK')
        assert institution.name == name
        assert institution.code == code
        assert institution.ror_id == ror_id

    @responses.activate
    @pytest.mark.django_db
    def test_multiple_mixed(self):
        command = Command()
        nhm_name = 'Natural History Museum, London'
        nhm_code = 'NHMUK'
        nhm_ror_id = '039zvsn29'
        Institution(name=nhm_name, code=nhm_code, ror_id='a different ROR ID').save()
        nhm_mock_result = {
            'count': 1,
            'results': [create_gbif_data(nhm_name, nhm_code, nhm_ror_id)]
        }
        responses.add(responses.GET, GBIF_REGISTRY_API_URL.format('NHMUK'), json=nhm_mock_result)

        mfn_name = 'Museum für Naturkunde'
        mfn_code = 'MfN'
        mfn_mock_result = {
            'count': 1,
            'results': [create_gbif_data(mfn_name, mfn_code)]
        }
        responses.add(responses.GET, GBIF_REGISTRY_API_URL.format('MfN'), json=mfn_mock_result)

        command.handle(codes=('NHMUK', 'MfN'))

        assert Institution.objects.count() == 2
        nhm = Institution.objects.get(code='NHMUK')
        assert nhm.name == nhm_name
        assert nhm.code == nhm_code
        assert nhm.ror_id == nhm_ror_id
        mfn = Institution.objects.get(code='MfN')
        assert mfn.name == mfn_name
        assert mfn.code == mfn_code
        assert mfn.ror_id == MISSING_ROR_ID

    @responses.activate
    @pytest.mark.django_db
    def test_no_results(self):
        command = Command()
        responses.add(responses.GET, GBIF_REGISTRY_API_URL.format('NHMUK'),
                      json={'count': 0, 'results': []})

        command.handle(codes=('NHMUK',))

        assert Institution.objects.count() == 0

    @responses.activate
    @pytest.mark.django_db
    def test_too_many_results(self):
        command = Command()
        responses.add(responses.GET, GBIF_REGISTRY_API_URL.format('NHMUK'),
                      json={'count': 2, 'results': [
                          create_gbif_data('a', 'b'),
                          create_gbif_data('c', 'd')
                      ]})

        command.handle(codes=('NHMUK',))

        assert Institution.objects.count() == 0
