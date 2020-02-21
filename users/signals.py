from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone


@receiver(user_logged_in, dispatch_uid="last_login_stamper")
def user_logged_in_successfully(sender, request, user, **kwargs):
    user.last_login = timezone.now()
    user.save()
