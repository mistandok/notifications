from django.db import models

from config.mixins import TimeStampedModel


class Template(TimeStampedModel):
    name = models.CharField(verbose_name="Название шаблона", max_length=255, null=True)
    html = models.TextField(verbose_name="HTML шаблон", null=True)

    class Meta:
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблоны"

    def __str__(self):
        return f"{self.name}"


class NotifyType(TimeStampedModel):
    name = models.CharField(verbose_name="Тип уведомления")
    slug = models.CharField(verbose_name="Слаг")
    template = models.ForeignKey(
        Template, verbose_name="Шаблон", on_delete=models.SET_NULL, null=True
    )
    group = models.BooleanField(verbose_name="Групповое событие", default=False)

    class Meta:
        verbose_name = "Тип уведомления"
        verbose_name_plural = "Типы уведомлений"

    def __str__(self):
        return f"{self.name}"


class Notify(TimeStampedModel):
    class StatusType(models.TextChoices):
        WAITING = "WA", "Ожидает отправки"
        SENDING = "SE", "Отправляется"
        SENDED = "SD", "Отправлено"
        ERROR = "ER", "Ошибка отправки"

    notify_type = models.ForeignKey(
        NotifyType, verbose_name="Тип уведомления", on_delete=models.SET_NULL, null=True
    )
    content = models.JSONField(verbose_name="Контент", null=True, blank=True)
    status = models.CharField(
        verbose_name="Статус",
        max_length=2,
        choices=StatusType.choices,
        null=True,
    )
    error_text = models.TextField(verbose_name="Текст ошибки отправки")
    retry_count = models.IntegerField(verbose_name="Попыток отправки", default=0)
    next_retry = models.DateTimeField(
        verbose_name="Следующая попытка отправки", null=True, blank=True
    )

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"{self.notify_type.__str__()}"


class Mailing(TimeStampedModel):
    class MailingPeriod(models.TextChoices):
        ONE_WEEK = "OW", "Раз в неделю"
        ONE_MONTH = "OM", "Раз в месяц"

    notify_type = models.ForeignKey(
        NotifyType, verbose_name="Тип уведомления", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(verbose_name="Название рассылки", max_length=255, null=True)
    period = models.CharField(
        verbose_name="Переодичность рассылки",
        max_length=2,
        choices=MailingPeriod.choices,
        null=True,
    )
    next_send = models.DateTimeField(
        verbose_name="Следующая рассылка", null=True, blank=True
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"{self.name}"
