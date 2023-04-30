import abc
from functools import lru_cache

from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives

from notify.models import Notify
from django.utils.html import strip_tags


class SenderProvider(abc.ABC):
    """
    Абстрактный класс для определения провайдера отправки уведомления
    """

    @property
    @abc.abstractmethod
    def provider_name(self):
        """
        Свойство с именем провайдера для его определния
        """
        pass

    @abc.abstractmethod
    def send(self, data: list, notify: Notify):
        """
        Функция отправки уведомления
        @param data: данные для уведомления
        @param notify: объект уведомления
        """
        pass


class MailProvider(SenderProvider):
    """Класс для отправки через почту россии)"""

    provider_name = "mail"

    def send(self, data: list, notify: Notify):
        """
        Формирует шаблоны для отправки и передает в отправку.
        Устанавливает соединенеие с почтовым сервером и отправляет пачку сообщений.
        @param data: Данные для отправки формата
        [
          {'email': 'bexram33@mail.ru',
           'surname': 'Ilya',
           ...},
        ...]

        @param notify: экземляр уведомления
        """
        template = notify.notify_type.template.html
        with get_connection(
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            fail_silently=True,
        ) as connection:
            messages = []
            for user in data:
                user_template = template

                for key, value in user.items():
                    if value:
                        user_template = user_template.replace(key, value)

                plain_message = strip_tags(user_template)
                message = EmailMultiAlternatives(
                    notify.notify_type.name,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [
                        user.get("email"),
                    ],
                )
                message.attach_alternative(user_template, "text/html")
                messages.append(message)

            return connection.send_messages(messages)


@lru_cache()
def get_sender_by_provider(provider_name, *args, **kwargs):
    """
    Получает провайдера по его названию
    @param provider_name: имя провайдера
    @param args:
    @param kwargs:
    @return:
    """
    for provider_cls in SenderProvider.__subclasses__():
        if provider_cls.provider_name == provider_name:
            return provider_cls(*args, **kwargs)
    raise KeyError("Не реализован провайдер")
