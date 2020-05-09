"""
Django settings for nabard project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os


def get_env(key, default):
    """
    Get environment variables. Keys are prefixed with APP.
    """
    return os.getenv(f"APP_{key}", default)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = get_env("SECRET_KEY", "qfzzh=d35pus17924)rpo)7iksoa!vt9gcyb^dna_-@j0t16gt")

DEBUG = get_env("DEBUG", "true").lower() == "true"

DOMAIN = get_env("DOMAIN", "")

ALLOWED_HOSTS = [] if DEBUG else [DOMAIN]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "users.apps.UsersConfig",
    "games.apps.GamesConfig",
    "robots.apps.RobotsConfig",
    "matches.apps.MatchesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nabard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nabard.wsgi.application"

AUTH_USER_MODEL = "users.User"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "USER": get_env("DB_USER", "nabard"),
        "PASSWORD": get_env("DB_PASS", "nabard"),
        "HOST": get_env("DB_HOST", "localhost"),
        "PORT": get_env("DB_PORT", "5432"),
        "NAME": get_env("DB_NAME", "nabard"),
        "TEST": {"NAME": "test"},
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = get_env("LANG", "en-us")

TIME_ZONE = get_env("TIMEZONE", "UTC")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = None if DEBUG else os.path.join(BASE_DIR, "static")

# API

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_VERSION": 1.0,
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.CursorPagination",
    "PAGE_SIZE": 20,
}

# Media files

AWS_ACCESS_KEY_ID = get_env("S3_ACCESS_KEY", "NABARD123456")
AWS_SECRET_ACCESS_KEY = get_env("S3_SECRET_KEY", "NABARD123456")
CODES_BUCKET_NAME = "codes"
AWS_S3_SECURE_URLS = False
AWS_DEFAULT_ACL = None
AWS_S3_ENDPOINT_URL = get_env("S3_ENDPOINT", "http://localhost:9000")

# Docker

DOCKER_BASE_URL = get_env("DOCKER_BASE_URL", "unix:///var/run/docker.sock")
DOCKER_MATCH_RUNNER_IMAGE = get_env(
    "DOCKER_MATCH_RUNNER_IMAGE", "nabardio/match-runner"
)

# Celery

CELERY_BROKER_URL = get_env("CELERY_BROKER_URL", "amqp://")
CELERY_RESULT_BACKEND = get_env("CELERY_RESULT_BACKEND", "rpc://")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# Email

EMAIL_USE_TLS = True
EMAIL_HOST = get_env("EMAIL_HOST", "")
EMAIL_HOST_USER = get_env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = get_env("EMAIL_HOST_PASSWORD", "")
EMAIL_PORT = get_env("EMAIL_PASSWORD", "")
