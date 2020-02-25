from datetime import timedelta

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            "id",
            "start_at",
            "finished_at",
            "game",
            "home_robot",
            "away_robot",
            "home_score",
            "away_score",
            "runner_log",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "finished_at",
            "game",
            "home_score",
            "away_score",
            "runner_log",
            "created_at",
            "updated_at",
        )

    def validate_home_robot(self, value):
        if value.owner != self.context["request"].user:
            raise serializers.ValidationError(
                _("home_robot must be one of your robots.")
            )
        return value

    def validate_away_robot(self, value):
        if value.owner == self.context["request"].user:
            raise serializers.ValidationError(
                _("away_robot must not be one of your robots.")
            )
        return value

    def validate_start_at(self, value):
        if value < timezone.now() + timedelta(minutes=1):
            raise serializers.ValidationError(
                _("start_at must be at least 1 minute from now.")
            )
        return value

    def validate(self, data):
        if data["home_robot"].game != data["away_robot"].game:
            raise serializers.ValidationError(
                _("home_robot and away_robot must play the same game")
            )
        data["game"] = data["home_robot"].game
        return data
