from django.contrib import admin

from nabard.admin import Admin

from . import models


@admin.register(models.Match)
class MatchAdmin(Admin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    readonly_fields,
                    "start_at",
                    "finished_at",
                    "game",
                    "home_robot",
                    "away_robot",
                    "home_score",
                    "away_score",
                    "runner_log",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("start_at", "game", "home_robot", "away_robot"),
            },
        ),
    )

    list_display = ("home_robot", "away_robot", "game", "start_at", "finished_at")
    list_filter = ("home_robot", "away_robot", "game", "start_at", "finished_at")
    ordering = ("finished_at",)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
