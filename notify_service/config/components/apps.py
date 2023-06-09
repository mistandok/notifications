from django.conf import settings

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "notify.apps.NotifyConfig",
    "django_celery_beat",
    "ckeditor",
]
if settings.DEBUG:
    INSTALLED_APPS += []
