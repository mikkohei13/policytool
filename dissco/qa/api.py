from django.conf import settings
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response

from qa.packs import PackProvider, PackTypeDoesNotExist, load_providers, Answer

PROVIDERS = load_providers(settings.QA_PACK_PROVIDERS)


def get_provider(pack_type: str) -> PackProvider:
    if pack_type not in PROVIDERS:
        raise PackTypeDoesNotExist()
    return PROVIDERS[pack_type]


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_packs(request: Request, responder_id: int, pack_type: str) -> Response:
    provider = get_provider(pack_type)
    if not provider.has_permission(request.user.institutionuser, responder_id):
        raise PermissionDenied()
    return Response([pack.to_dict() for pack in provider.get_packs(responder_id)])


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_pack(request: Request, responder_id: int, pack_type: str, pack_id: int) -> Response:
    provider = get_provider(pack_type)
    if not provider.has_permission(request.user.institutionuser, responder_id):
        raise PermissionDenied()
    return Response(provider.get_pack(responder_id, pack_id).to_dict())


@api_view(['POST', 'DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def handle_answer(request: Request, responder_id: int, pack_type: str, pack_id: int,
                  question_id: int) -> Response:
    provider = get_provider(pack_type)
    if not provider.has_permission(request.user.institutionuser, responder_id):
        raise PermissionDenied()
    match request.method:
        case 'POST':
            return create_answer(provider, responder_id, pack_id, question_id, request.data)
        case 'DELETE':
            return delete_answer(provider, responder_id, pack_id, question_id)


def create_answer(provider: PackProvider, responder_id: int, pack_id: int, question_id: int,
                  data: dict) -> Response:
    answer = Answer.from_dict(data)
    provider.save_answer(responder_id, pack_id, question_id, answer)
    return Response(status=201)


def delete_answer(provider: PackProvider, responder_id: int, pack_id: int,
                  question_id: int) -> Response:
    provider.delete_answer(responder_id, pack_id, question_id)
    return Response(status=200)


@api_view(['PUT'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def finish_pack(request: Request, responder_id: int, pack_type: str, pack_id: int) -> Response:
    provider = get_provider(pack_type)
    if not provider.has_permission(request.user.institutionuser, responder_id):
        raise PermissionDenied()
    # an empty/request without a finished field implies completion
    state = request.data.get('finished', True)
    provider.finish(responder_id, pack_id, state)
    return Response(status=200)
