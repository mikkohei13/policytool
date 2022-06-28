from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.models import Institution
from common.serializers import InstitutionSerializer, InstitutionUserSerializer, UserSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def whoami(request: Request) -> Response:
    user = request.user
    if hasattr(user, 'institutionuser'):
        return Response(InstitutionUserSerializer(request.user.institutionuser).data)
    else:
        user_data = UserSerializer(user).data
        return Response({'user': user_data})
