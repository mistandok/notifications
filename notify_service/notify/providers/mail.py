import os

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from notify.models import Notify
from notify.providers.provider import SenderProvider


class MailProvider(SenderProvider):
    @property
    def provider_name(self):
        return "mail"

    def send(self, data: dict, notify: Notify):
        html_message = render_to_string(notify.notify_type.template, data)
        plain_message = strip_tags(html_message)
        send_mail(
            subject=data.get("subject"),
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            #TODO: передедать получателя
            recipient_list=[data.get("recipient")],
            fail_silently=False,
            html_message=html_message,
        )
