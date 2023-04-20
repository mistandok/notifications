from config.celery import app
from notify.models import Notify, NotifyType
from notify.providers.provider import SenderProvider


@app.task
def treatment_api_data(data: dict):
    """Обрабатывает данные от апи"""
    new_notify: Notify = Notify.objects.create(content=data)
    if notify_type := NotifyType.objects.filter(slug=data.get("type")):
        if not notify_type.template:
            new_notify.error_text = (
                f"У типа уведомлений {notify_type.name} не задан шаблон"
            )
            new_notify.status = Notify.StatusType.ERROR
        else:
            send_message.delay(data)
    else:
        new_notify.error_text = f"Не существует тип уведомлений {notify_type.name}"
        new_notify.status = Notify.StatusType.ERROR
    new_notify.save()


@app.task
def send_message(data: dict):
    """Выбирает провайдера и отправляет уведомление через него"""
    provider = SenderProvider.get_provider(data.pop("provider"))
    provider.send(data)


@app.task
def collect_person_data(data: dict):
    """Собирает данные для персональной рассылки"""
    pass


@app.task
def collect_group_data(data: dict):
    """Собирает данные для групповой рассылки"""
    pass