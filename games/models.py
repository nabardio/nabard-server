from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from nabard.models import Model
from nabard.storages import CodeStorage


class Game(Model):
    def game_code_path(self, filename):
        return f"games/{self.pk}/{filename}"

    name = models.CharField(
        _("name"),
        max_length=150,
        unique=True,
        help_text=_("Required. 150 characters or fewer."),
        error_messages={"unique": _("A game with that name already exists.")},
    )
    description = models.CharField(max_length=1024, blank=True, null=True)
    instruction = models.TextField()
    code = models.FileField(
        _("code"),
        storage=CodeStorage(),
        upload_to=game_code_path,
        validators=[FileExtensionValidator(["py"])],
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="games", on_delete=models.CASCADE
    )
