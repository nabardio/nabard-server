from django.conf import settings
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from nabard.models import Model
from nabard.storages import CodeStorage


class Robot(Model):
    def robot_code_path(self, filename):
        return f"codes/robots/{self.pk}/{filename}"

    name = models.CharField(
        "name",
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and " "./-/_ only."
        ),
        validators=[RegexValidator(regex=r"^[\w\.\-]+$")],
        error_messages={"unique": _("A robot with that name already exists.")},
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="robots", on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        "games.Game", related_name="robots", on_delete=models.CASCADE
    )
    code = models.FileField(
        _("code"),
        blank=True,
        upload_to=robot_code_path,
        storage=CodeStorage(),
        validators=[FileExtensionValidator(["py"])],
    )
