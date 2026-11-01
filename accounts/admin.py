from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import AdminUserCreationForm, AdminUserChangeForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    model = User
    list_display = ('username', 'is_staff', 'is_active', 'environment')
    list_filter = ('is_staff', 'is_active', 'environment')
    search_fields = ('username',)

    fieldsets = (
        (
            'Información Personal', {
                'fields': (
                    'username',
                    'password',
                    'first_name',
                    'last_name',
                    'email',
                    'date_joined',
                    'last_login'
                )
            }
         ),
        (
            'Permisos de acceso', {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                    'environment'
                )
            }
        ),

    )

    search_fields = ('username',)
    ordering = ('id',)
