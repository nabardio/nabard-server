from django.db import models
from django.utils.translation import gettext_lazy as _

from nabard.models import Model


class Match(Model):
    start_at = models.DateTimeField(_("start at"))
    finished_at = models.DateTimeField(_("finished at"), null=True, blank=True)
    home_score = models.FloatField(default=0)
    away_score = models.FloatField(default=0)
    runner_log = models.TextField(null=True)
    game = models.ForeignKey(
        "games.Game", related_name="matches", on_delete=models.CASCADE
    )
    home_robot = models.ForeignKey(
        "robots.Robot", related_name="home_matches", on_delete=models.CASCADE
    )
    away_robot = models.ForeignKey(
        "robots.Robot", related_name="away_matches", on_delete=models.CASCADE
    )
