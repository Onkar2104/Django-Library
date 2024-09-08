from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserAdminCreationForm, UserAdminChangeForm

class UserAdmin(BaseUserAdmin):
    search_fields = ['email']
    form = UserAdminChangeForm  # For updating users
    add_form = UserAdminCreationForm  # For creating new users

    # Specify which fields to display in the admin list view
    list_display = ['email', 'is_staff', 'is_active', 'is_superuser']

    # Specify fields and fieldsets for add/change forms
    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password', 'password_2', 'is_staff', 'is_active'),
        }),
    )

    ordering = ['email']  # Specify default ordering by email


admin.site.register(User, UserAdmin)
