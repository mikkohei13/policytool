from rest_framework import permissions, authentication
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from maturity import serializers
from maturity.models import Responder


class ResponderAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, responder_id: int | None):
        if responder_id is not None:
            responder = Responder.objects.get(owner=request.user, id=responder_id)
            serializer = serializers.ResponderSerializer(responder)
        else:
            responders = Responder.objects.filter(owner=request.user)
            serializer = serializers.ResponderSerializer(responders, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        data = {**request.data, 'owner': request.user.id}

        serializer = serializers.ResponderSerializer()
        valid_data = serializer.run_validation(data)

        responder = Responder(**valid_data)
        responder.save()
        return Response({'id': responder.id}, status=201)
