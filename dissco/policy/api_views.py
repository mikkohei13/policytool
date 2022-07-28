from rest_framework import permissions, authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Institution
from policy import models
from policy import serializers
from policy.alignment import calculate_alignment
from policy.models import InstitutionPolicyArea, ServicePolicyMapping


@api_view(['GET'])
def get_dissco_service_list(request: Request) -> Response:
    services = models.Service.objects.prefetch_related('components').all()
    serializer = serializers.ServiceSerializer(services, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_dissco_service(request: Request, service_id: int) -> Response:
    service = models.Service.objects.prefetch_related('components').get(id=service_id)
    serializer = serializers.ServiceSerializer(service)
    return Response(serializer.data)


@api_view(['GET'])
def get_dissco_policy_list(request: Request) -> Response:
    policies = models.PolicyArea.objects \
        .prefetch_related('category') \
        .prefetch_related('components') \
        .all()
    serializer = serializers.PolicyAreaSerializer(policies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_institution_public_policy_list(request: Request) -> Response:
    # TODO: filter for public policies
    policies = models.InstitutionPolicyArea.objects.all()
    serializer = serializers.InstitutionPolicyAreaSerializer(policies, many=True)
    return Response(serializer.data)


def create_alignment_response_dict(mapping: ServicePolicyMapping, institution: Institution) -> dict:
    return {
        'mapping': mapping.id,
        'service': mapping.service_component.service_id,
        'policy': mapping.policy_component.policy_area_id,
        'policy_name': mapping.policy_component.policy_area.name,
        'service_component': mapping.service_component_id,
        'policy_component': mapping.policy_component_id,
        'status': calculate_alignment(mapping, institution).to_dict(),
    }


# TODO: should this be public?
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_institution_alignment(request: Request) -> Response:
    institution = request.user.institutionuser.institution
    alignment = [
        create_alignment_response_dict(mapping, institution)
        for mapping in models.ServicePolicyMapping.objects.all()
    ]
    return Response(alignment)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_institution_alignment_mapping(request: Request, mapping_id: int) -> Response:
    institution = request.user.institutionuser.institution
    mapping = models.ServicePolicyMapping.objects.get(id=mapping_id)
    alignment = create_alignment_response_dict(mapping, institution)
    return Response(alignment)


class InstitutionPolicyAreaAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        institution = request.user.institutionuser.institution
        serializer = serializers.InstitutionPolicyAreaSerializer(institution.policies, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        institution = request.user.institutionuser.institution

        data = {**request.data, 'institution': institution.pk}

        serializer = serializers.InstitutionPolicyAreaSerializer()
        valid_data = serializer.run_validation(data)

        policy = InstitutionPolicyArea(**valid_data)
        policy.save()
        return Response({'id': policy.id}, status=201)
