import os
from pathlib import Path
from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    "components/database.py",
    "components/apps.py",
    "components/middleware.py",
    "components/mail.py",
)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "SECRET_KEY")

DEBUG = os.environ.get("DEBUG", False) == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOST", "127.0.0.1,localhost").split(",")

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INTERNAL_IPS = [
    "127.0.0.1",
]

USER_PREFERENCES_SERVICE_URL = os.environ.get(
    "USER_PREFERENCES_SERVICE_URL", "localhost:5000"
)
USER_PREFERENCES_SERVICE_TOKEN = os.environ.get(
    "USER_PREFERENCES_SERVICE_TOKEN", "token"
)

AUTH_SERVICE_URL = os.environ.get("AUTH_SERVICE_URL", "localhost:60000")
AUTH_SERVICE_TOKEN = os.environ.get("AUTH_SERVICE_TOKEN", "token")

CELERY_BROKER_URL = f'amqp://{os.getenv("RABBITMQ_DEFAULT_USER", "sampleproject")}:{os.getenv("RABBITMQ_DEFAULT_PASS", "sampleproject")}@rabbit:5672'
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


if not DEBUG:
    CKEDITOR_BASEPATH = os.path.join(BASE_DIR, "static/ckeditor/ckeditor/")
