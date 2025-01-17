from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# If you have a custom Institution model, import it
from .models import Institution  # adjust the import path as needed

# Extend the UserAdmin to include institution field
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'institution', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'institution')
    
    # Add institution to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Institution Information', {'fields': ('institution',)}),
    )

# Register the custom admin class
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register the Institution model if you have one
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',) 