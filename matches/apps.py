from django.apps import AppConfig


class MatchesConfig(AppConfig):
    name = "matches"

    def ready(self):
        from . import signals
