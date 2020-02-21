from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class CodeStorage(S3Boto3Storage):
    bucket_name = settings.CODES_BUCKET_NAME
