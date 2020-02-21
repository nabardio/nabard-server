from django.contrib import admin

from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    readonly_fields,
                    "owner",
                    "name",
                    "description",
                    "instruction",
                    "code",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("owner", "name", "description", "instruction", "code"),
            },
        ),
    )

    list_display = ("name", "description", "owner")
    ordering = ("name",)
    search_fields = ("name", "description")
