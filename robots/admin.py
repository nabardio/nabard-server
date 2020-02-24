from django.contrib import admin

from nabard.admin import Admin

from .models import Robot


@admin.register(Robot)
class RobotAdmin(Admin):
    readonly_fields = ("id", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": (readonly_fields, "owner", "game", "name", "code")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("owner", "game", "name", "code")}),
    )

    list_display = ("name", "game", "owner")
    ordering = ("name",)
    search_fields = ("name",)
