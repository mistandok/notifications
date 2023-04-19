from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)

    class Meta:
        abstract = True
