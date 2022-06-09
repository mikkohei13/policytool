from django.contrib.auth.models import User
from rest_framework import serializers

from common.models import Institution


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'code', 'wikidata_id']
