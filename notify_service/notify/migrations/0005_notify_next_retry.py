# Generated by Django 4.2 on 2023-04-22 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0004_notify_retry_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='notify',
            name='next_retry',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Следующая попытка отправки'),
        ),
    ]
