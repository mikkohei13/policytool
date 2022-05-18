from django.contrib import admin

from policy.models import Service, ServiceComponent, PolicyCategory, PolicyArea, PolicyComponent, \
    PolicyComponentOption, InstitutionPolicyArea, InstitutionPolicyOwner, \
    InstitutionPolicyLanguage, InstitutionPolicyComponent, ServicePolicyMapping

admin.site.register(Service)
admin.site.register(ServiceComponent)
admin.site.register(PolicyCategory)
admin.site.register(PolicyArea)
admin.site.register(PolicyComponent)
admin.site.register(PolicyComponentOption)
admin.site.register(InstitutionPolicyArea)
admin.site.register(InstitutionPolicyOwner)
admin.site.register(InstitutionPolicyLanguage)
admin.site.register(InstitutionPolicyComponent)
admin.site.register(ServicePolicyMapping)
