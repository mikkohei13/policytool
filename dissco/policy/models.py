from django.db import models

from common.models import Institution


class Service(models.Model):
    description = models.TextField()
    name = models.TextField()


class PolicyArea(models.Model):
    name = models.TextField()
    number = models.IntegerField()
    scope = models.TextField()  # TODO: ?


class PolicyCategory(models.Model):
    name = models.TextField()
    policy_area = models.ForeignKey(PolicyArea, on_delete=models.CASCADE)


class ServiceCategory(models.Model):
    description = models.TextField()
    name = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class ServiceSubcategory(models.Model):
    description = models.TextField()
    name = models.TextField()
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)


class ServiceSubcategoryPolicyComponent(models.Model):
    value = models.TextField()  # TODO: ?
    rules = models.TextField()  # TODO: ?
    subcategory = models.ForeignKey(ServiceSubcategory, on_delete=models.CASCADE)


class PolicyComponent(models.Model):
    description = models.TextField()
    value_type = models.TextField()  # TODO: type?
    policy_area = models.ForeignKey(PolicyArea, on_delete=models.CASCADE)
    service_subcategory_policy_component = models.ForeignKey(ServiceSubcategoryPolicyComponent,
                                                             on_delete=models.CASCADE)


class PolicyComponentOption(models.Model):
    value = models.TextField()  # TODO: type?
    policy_component = models.ForeignKey(PolicyComponent, on_delete=models.CASCADE)
    service_subcategory_policy_component = models.ForeignKey(ServiceSubcategoryPolicyComponent,
                                                             on_delete=models.CASCADE)


class InstitutionPolicyArea(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    policy_exists = models.BooleanField()
    owner = models.TextField()  # TODO: ?
    signatory = models.TextField()  # TODO: ?
    documentation_exists = models.BooleanField()
    documentation_next_review_date = models.DateTimeField()
    documentation_language = models.CharField(max_length=2)  # TODO: choice?
    documentation_public = models.BooleanField()
    documentation_shareable = models.BooleanField()
    documentation_provided = models.BooleanField()
    documentation_details = models.TextField()
    policy_summary = models.TextField()
    additional_notes = models.TextField()
    policy_area = models.ForeignKey(PolicyArea, on_delete=models.CASCADE)


class InstitutionPolicyComponent(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    policy_component = models.ForeignKey(PolicyComponent, on_delete=models.CASCADE)
    value = models.TextField()  # TODO: ?
