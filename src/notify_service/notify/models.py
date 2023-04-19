from django.db import models

from src.notify_service.config.mixins import TimeStampedModel


# Create your models here.
class Notify(TimeStampedModel):
    class NotifyType(models.TextChoices):
        AUTH = "AU", "Авторизация"
        TOP_FILMS = "TF", "Рассылка топ фильмов"
        # для примера были взяты только такие типы

    class StatusType(models.TextChoices):
        WAITING = "WA", "Ожидает отправки"
        SENDING = "SE", "Отправляется"
        SENDED = "SD", "Отправлено"
        ERROR = "ER", "Ошибка отправки"

    t = models.CharField(
        verbose_name="Тип уведомления",
        max_length=2,
        choices=NotifyType.choices,
        null=True,
    )
    content = models.JSONField(verbose_name="Контент", null=True, blank=True)
    status = models.CharField(
        verbose_name="Статус",
        max_length=2,
        choices=StatusType.choices,
        null=True,
    )


class Template(TimeStampedModel):
    name = models.CharField(verbose_name="Название шаблона", max_length=255, null=True)
    html = models.TextField(verbose_name="HTML шаблон", null=True)


class Mailing(TimeStampedModel):
    pass
