import os

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.mail.ru"
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.environ.get("EMAIL_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER