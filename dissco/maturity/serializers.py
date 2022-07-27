from django.contrib.auth.models import User
from rest_framework import serializers

from maturity import models


TEAM_NAME_UNIQUENESS_ERROR = '''The name must be unique among your existing teams (this applies 
regardless of the type of team)'''


class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Responder
        fields = ['id', 'type', 'name', 'comment', 'owner']

    def validate(self, data):
        name: str = data.get('name')
        owner: User = data.get('owner')

        if models.Responder.objects.filter(owner=owner, name=name).exists():
            raise serializers.ValidationError({'name': TEAM_NAME_UNIQUENESS_ERROR})

        return super().validate(data)
