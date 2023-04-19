import os

from django.core.mail import send_mail

from src.notify_service.notify.providers.provider import SenderProvider


class MailProvider(SenderProvider):
    @property
    def provider_name(self):
        return "mail"

    def send(self, data: dict):
        send_mail(
            subject=data.get("subject"),
            html_message=data.get("html_message"),
            message=data.get("message"),
            from_email=os.environ.get("EMAIL_USER"),
            recipient_list=[data.get("recipient")],
            fail_silently=False,
        )
