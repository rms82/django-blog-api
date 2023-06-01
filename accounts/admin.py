from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Profile


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['username', 'email', 'age', 'is_staff']
    fieldsets = (
        ('Authentication', {
            "fields": (
                'username', 'email', 'password', 'age',
            ),
        }),

        ('permissions', {
            "fields": (
                'is_staff', 'is_active',
            ),
        }),

        ('permissions groups', {
            "fields": (
                'groups', 'user_permissions',
            ),
        }),

        ('Important dates', {
            'fields': ('last_login', 'date_joined',
            ),
        }),

    )
    add_fieldsets = (
        ('Register', {
            "fields": (
                'username', 'email', 'password1', 'password2', 'age', 'is_staff', 'is_active',
            ),
        }),
    )


admin.site.register(Profile)
