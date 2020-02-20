from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    readonly_fields = ("id", "created_at", "updated_at", "last_login")
    fieldsets = (
        (None, {"fields": ("password", readonly_fields)}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "username", "email")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("username", "first_name", "last_name", "email")
    ordering = ("last_name", "first_name")
    search_fields = ("username", "email", "first_name", "last_name")
