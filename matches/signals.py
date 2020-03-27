from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Match
from .tasks import run_match


@receiver(pre_save, sender=Match, dispatch_uid="matches.signals.revoke_scheduled_task")
def revoke_scheduled_task(sender, instance, **kwargs):
    if instance.start_at_changed():
        instance.scheduled_task.revoke()
        del instance.scheduled_task

    if not instance.scheduled_task:
        instance.scheduled_task = run_match.apply_async(
            args=(instance.pk,), eta=instance.start_at
        )
