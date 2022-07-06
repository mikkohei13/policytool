from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.models import Institution
from common.serializers import InstitutionSerializer, UserSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def whoami(request: Request) -> Response:
    user = request.user
    data = {
        'user': UserSerializer(user).data,
    }
    if hasattr(user, 'institutionuser'):
        data['institution'] = InstitutionSerializer(request.user.institutionuser.institution).data
    return Response(data)
