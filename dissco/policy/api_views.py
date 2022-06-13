from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Institution
from policy import models
from policy import serializers


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Service.objects.prefetch_related('components').all()
    serializer_class = serializers.ServiceSerializer
    filterset_fields = ['name']


class PolicyAreaViewSet(viewsets.ModelViewSet):
    queryset = models.PolicyArea.objects.prefetch_related('category').all()
    serializer_class = serializers.PolicyAreaSerializer
    filterset_fields = ['name', 'category']

    @action(detail=True)
    def components(self, request: Request, pk=None):
        policy_area = self.get_object()
        serializer = serializers.PolicyComponentSerializer(policy_area.components, many=True)
        return Response(serializer.data)


class InstitutionPolicyAreaAPIView(APIView):

    def get(self, request: Request, institution_id: int):
        institution = Institution.objects.get(id=institution_id)
        serializer = serializers.InstitutionPolicyAreaSerializer(institution.policies, many=True)
        return Response(serializer.data)


class InstitutionPolicyComponentAPIView(APIView):

    def get(self, request: Request, institution_id: int):
        institution = Institution.objects.get(id=institution_id)
        serializer = serializers.InstitutionPolicyComponentSerializer(institution.components,
                                                                      many=True)
        return Response(serializer.data)
