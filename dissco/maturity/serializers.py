from rest_framework import serializers

from maturity import models


class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Responder
        fields = ['id', 'type', 'name', 'comment', 'owner']
