from django.contrib import admin
from django.contrib.auth.models import User

from common.models import Institution, InstitutionUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class InstitutionUserInline(admin.StackedInline):
    model = InstitutionUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (InstitutionUserInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Institution)
