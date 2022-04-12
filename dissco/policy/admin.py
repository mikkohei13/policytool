from django.contrib import admin

from policy.models import PolicyArea, InstitutionPolicyArea, InstitutionPolicyComponent, \
    PolicyCategory, PolicyComponentOption, PolicyComponent, ServiceSubcategoryPolicyComponent, \
    ServiceCategory, ServiceSubcategory, Service

admin.site.register(PolicyArea)
admin.site.register(InstitutionPolicyArea)
admin.site.register(InstitutionPolicyComponent)
admin.site.register(PolicyCategory)
admin.site.register(PolicyComponentOption)
admin.site.register(PolicyComponent)
admin.site.register(ServiceSubcategoryPolicyComponent)
admin.site.register(ServiceCategory)
admin.site.register(ServiceSubcategory)
admin.site.register(Service)
