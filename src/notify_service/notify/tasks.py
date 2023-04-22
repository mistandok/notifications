import requests

from config import settings
from config.celery import app
from notify.models import Notify, NotifyType
from notify.providers.provider import SenderProvider


@app.task
def treatment_api_data(data: dict):
    """Обрабатывает данные от апи"""
    new_notify: Notify = Notify.objects.create(content=data)
    if notify_type := NotifyType.objects.filter(slug=data.get("notify_type")):
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
def send_message(notify_data: dict, user_data: dict, provider: str, notify_id: int):
    """Выбирает провайдера и отправляет уведомление через него"""
    new_notify = Notify.objects.get(id=notify_id)
    try:
        provider = SenderProvider.get_provider(provider)
        notify_data |= user_data
        provider.send(notify_data, new_notify)
    except Exception as e:
        new_notify.error_text = str(e)
        new_notify.status = Notify.StatusType.ERROR
        new_notify.save()
    new_notify.status = Notify.StatusType.SENDED
    new_notify.save()


@app.task
def collect_person_data(data: dict, notify_id: int):
    """Собирает данные для персональной рассылки"""
    new_notify = Notify.objects.get(id=notify_id)
    new_notify.status = Notify.StatusType.SENDING
    new_notify.save()
    user_prefs = get_user_prefs([data.get("user_id")], notify_id)[0].get("preferences")
    provider = ""
    for notify_type in user_prefs:
        if notify_type.get("event_type") == data.get("notify_type"):
            provider = notify_type.get("provider")
            break
    user_data = get_user_prefs([data.get("user_id")], notify_id)[0]
    send_message.delay(
        notify_data=data, user_data=user_data, provider=provider, notify_id=notify_id
    )


@app.task
def collect_group_data(data: dict):
    """Собирает данные для групповой рассылки"""
    pass


def get_user_prefs(user_ids: list, notify_id: int) -> list | None:
    new_notify = Notify.objects.get(id=notify_id)
    if (
        settings.USER_PREFERENCES_SERVICE_URL
        and settings.USER_PREFERENCES_SERVICE_TOKEN
    ):
        response = requests.get(
            settings.USER_PREFERENCES_SERVICE_URL
            + "/preferences/api/v1/user-preferences/list",
            headers={
                "Authorization": "Bearer " + settings.USER_PREFERENCES_SERVICE_TOKEN
            },
            data={"user_ids": user_ids},
        )
        if response.status_code == 200:
            return response.json()
        else:
            new_notify.error_text = f"{response.status_code}: {response.text}"
            new_notify.status = Notify.StatusType.ERROR
            new_notify.save()
            return None

    else:
        new_notify.error_text = f"Не задан адрес или токен сервиса настроек"
        new_notify.status = Notify.StatusType.ERROR
        new_notify.save()
        return None


def get_user_data(user_ids: list, notify_id: int) -> list | None:
    new_notify = Notify.objects.get(id=notify_id)
    if settings.AUTH_SERVICE_URL and settings.AUTH_SERVICE_TOKEN:
        response = requests.get(
            settings.AUTH_SERVICE_URL + "/preferences/api/v1/user-preferences/list",
            headers={"Authorization": "Bearer " + settings.AUTH_SERVICE_TOKEN},
            data={"user_ids": user_ids},
        )
        if response.status_code == 200:
            return response.json()
        else:
            new_notify.error_text = f"{response.status_code}: {response.text}"
            new_notify.status = Notify.StatusType.ERROR
            new_notify.save()
            return None
    else:
        new_notify.error_text = f"Не задан адрес или токен сервиса авторизации"
        new_notify.status = Notify.StatusType.ERROR
        new_notify.save()
        return None
