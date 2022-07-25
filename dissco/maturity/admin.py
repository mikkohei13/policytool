from django.contrib import admin

from maturity import models

admin.site.register(models.Category)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Responder)
