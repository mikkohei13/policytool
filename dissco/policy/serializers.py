from rest_framework import serializers

from policy import models


class ServiceComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceComponent
        fields = ['id', 'name', 'description']


class ServiceSerializer(serializers.ModelSerializer):
    components = ServiceComponentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Service
        fields = ['id', 'name', 'description', 'url', 'components']


class PolicyComponentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PolicyComponentOption
        fields = ['id', 'value']


class PolicyComponentSerializer(serializers.ModelSerializer):
    options = PolicyComponentOptionSerializer(many=True, read_only=True)

    class Meta:
        model = models.PolicyComponent
        fields = ['id', 'name', 'question', 'description', 'type', 'options']


class PolicyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PolicyCategory
        fields = ['name', 'scope']


class PolicyAreaSerializer(serializers.ModelSerializer):
    # this produces a lot of repetition but I think it's better this way
    category = PolicyCategorySerializer(read_only=True)
    components = PolicyComponentSerializer(many=True, read_only=True)

    class Meta:
        model = models.PolicyArea
        fields = ['id', 'name', 'number', 'scope', 'category', 'components']


# TODO: should this be publicly available? (I think maybe no?)
class InstitutionPolicyOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstitutionPolicyOwner
        fields = ['name', 'role']


class InstitutionPolicyLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstitutionPolicyLanguage
        fields = ['code']


class InstitutionPolicyAreaSerializer(serializers.ModelSerializer):
    owners = InstitutionPolicyOwnerSerializer(many=True, read_only=True)
    languages = InstitutionPolicyLanguageSerializer(many=True, read_only=True)

    class Meta:
        model = models.InstitutionPolicyArea
        fields = ['id', 'name', 'status', 'documentation_date', 'documentation_next_review_date',
                  'documentation_public', 'documentation_shareable', 'documentation_details',
                  'policy_summary', 'additional_notes', 'institution', 'policy_area', 'owners',
                  'languages']


# TODO: should this be publicly available? (maybe?)
class InstitutionPolicyComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstitutionPolicyComponent
        fields = ['id', 'value', 'chosen_options', 'comment', 'institution', 'policy_component']


class ServicePolicyMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServicePolicyMapping
        fields = ['id', 'service_component', 'policy_component']
