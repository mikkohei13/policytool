from rest_framework import viewsets

from common.models import Institution
from common.serializers import InstitutionSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
