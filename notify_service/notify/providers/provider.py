import abc
from functools import lru_cache

from django.conf import settings

from notify.models import Notify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class SenderProvider(abc.ABC):
    @property
    @abc.abstractmethod
    def provider_name(self):
        pass

    @abc.abstractmethod
    def send(self, data: dict, notify: Notify):
        pass


@lru_cache()
def get_sender_by_provider(provider_name, *args, **kwargs):
    for provider_cls in SenderProvider.__subclasses__():
        if provider_cls.provider_name == provider_name:
            return provider_cls(*args, **kwargs)
    raise KeyError("Не реализован провайдер")


class MailProvider(SenderProvider):
    provider_name = "mail"

    def send(self, data: dict, notify: Notify):
        template = notify.notify_type.template.html
        for key in data.keys():
            if data.get(key):
                template = template.replace(key, data.get(key))
        plain_message = strip_tags(template)
        send_mail(
            subject=data.get("subject"),
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            # TODO: передедать получателя
            recipient_list=[data.get("email")],
            fail_silently=False,
            html_message=template,
        )
