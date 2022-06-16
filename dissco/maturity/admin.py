from django.contrib import admin

from maturity import models

admin.site.register(models.Category)
admin.site.register(models.SubCategory)
admin.site.register(models.InstitutionSubCategory)
