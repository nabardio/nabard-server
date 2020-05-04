from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException
from rest_framework import status


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad Request (400).')
    default_code = 'bad_request'
