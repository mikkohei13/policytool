from django.contrib.auth.models import User
from rest_framework import serializers

from common.models import Institution, InstitutionUser


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'ror_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class InstitutionUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    institution = InstitutionSerializer(read_only=True)

    class Meta:
        model = InstitutionUser
        fields = ['user', 'institution']
