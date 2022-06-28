from django.conf import settings
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from common.models import Institution
from qa.packs import PackProvider, PackTypeDoesNotExist, load_providers, Answer

PROVIDERS = load_providers(settings.QA_PACK_PROVIDERS)


def get_provider(pack_type: str) -> PackProvider:
    if pack_type not in PROVIDERS:
        raise PackTypeDoesNotExist()
    return PROVIDERS[pack_type]


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_packs(request: Request, pack_type: str) -> Response:
    provider = get_provider(pack_type)
    institution = request.user.institutionuser.institution
    return Response([pack.to_dict() for pack in provider.get_packs(institution)])


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_pack(request: Request, pack_type: str, pack_id: int) -> Response:
    provider = get_provider(pack_type)
    institution = request.user.institutionuser.institution
    return Response(provider.get_pack(institution, pack_id).to_dict())


@api_view(['POST', 'DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def handle_answer(request: Request, pack_type: str, question_id: int) -> Response:
    provider = get_provider(pack_type)
    institution = request.user.institutionuser.institution
    match request.method:
        case 'POST':
            return create_answer(provider, institution, question_id, request.data)
        case 'DELETE':
            return delete_answer(provider, institution, question_id)


def create_answer(provider: PackProvider, institution: Institution, question_id: int,
                  data: dict) -> Response:
    answer = Answer.from_dict(data)
    provider.save_answer(institution, question_id, answer)
    return Response(status=201)


def delete_answer(provider: PackProvider, institution: Institution, question_id: int) -> Response:
    provider.delete_answer(institution, question_id)
    return Response(status=200)
