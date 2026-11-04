from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .forms import AdminUserChangeForm, AdminUserCreationForm
from .models import User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)
    filter_horizontal = ("permissions",)
    
    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "permissions":
            qs = kwargs.get("queryset", db_field.remote_field.model.objects)
            kwargs["queryset"] = qs.select_related("content_type")
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    form = AdminUserChangeForm
    add_form = AdminUserCreationForm
    model = User
    
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "environment")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "environment")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    list_filter_submit = True
    list_show_full_result_count = True
    compressed_fields = True
    list_fullwidth = True

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Información Personal"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permisos de acceso"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "environment",
                ),
            },
        ),
        (_("Fechas importantes"), {"fields": ("last_login", "date_joined")}),
    )
