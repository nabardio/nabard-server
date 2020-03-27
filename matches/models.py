from celery.result import AsyncResult
from django.db import models
from django.utils.translation import gettext_lazy as _

from nabard.models import Model


class Match(Model):
    start_at = models.DateTimeField(_("start at"))
    finished_at = models.DateTimeField(_("finished at"), null=True, blank=True)
    home_score = models.FloatField(default=0)
    away_score = models.FloatField(default=0)
    runner_log = models.TextField(null=True, blank=True)
    game = models.ForeignKey(
        "games.Game", related_name="matches", on_delete=models.CASCADE
    )
    home_robot = models.ForeignKey(
        "robots.Robot", related_name="home_matches", on_delete=models.CASCADE
    )
    away_robot = models.ForeignKey(
        "robots.Robot", related_name="away_matches", on_delete=models.CASCADE
    )

    _scheduled_task_id = models.CharField("scheduled task id", max_length=36, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_start_at = self.start_at

    def __str__(self):
        return f"{self.home_robot} vs {self.away_robot}"

    def start_at_changed(self):
        return self.__original_start_at != self.start_at

    @property
    def scheduled_task(self):
        if self._scheduled_task_id:
            return AsyncResult(self._scheduled_task_id)

    @scheduled_task.setter
    def scheduled_task(self, task):
        if isinstance(task, AsyncResult):
            self._scheduled_task_id = task.id

    @scheduled_task.deleter
    def scheduled_task(self):
        self._scheduled_task_id = None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.__original_start_at = self.start_at
