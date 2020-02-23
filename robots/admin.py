from django.contrib import admin

from .models import Robot


@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
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
