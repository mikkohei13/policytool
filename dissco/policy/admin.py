from django.contrib import admin

from policy import models

admin.site.register(models.Service)
admin.site.register(models.ServiceComponent)
admin.site.register(models.PolicyCategory)
admin.site.register(models.PolicyArea)
admin.site.register(models.PolicyComponent)
admin.site.register(models.PolicyComponentOption)
admin.site.register(models.InstitutionPolicyArea)
admin.site.register(models.InstitutionPolicyOwner)
admin.site.register(models.InstitutionPolicyLanguage)
admin.site.register(models.InstitutionPolicyComponent)
admin.site.register(models.ServicePolicyMapping)
