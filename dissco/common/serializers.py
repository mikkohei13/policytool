from rest_framework import serializers

from common.models import Institution


class InstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'code', 'wikidata_id']
