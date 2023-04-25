from datetime import timedelta
from http import HTTPStatus
from typing import Generator

import requests
from django.utils import timezone

from config import settings
from config.celery import app
from notify.models import Notify, NotifyType, Mailing
from notify.providers.provider import SenderProvider


@app.task
def treatment_api_data(data: dict):
    """Обрабатывает данные от апи"""
    new_notify: Notify = Notify.objects.create(content=data)
    if notify_type := NotifyType.objects.filter(slug=data.get("notify_type")).first():
        new_notify.notify_type = notify_type
        new_notify.save()
        if not notify_type.template:
            new_notify.error_text = (
                f"У типа уведомлений {notify_type.name} не задан шаблон"
            )
            new_notify.status = Notify.StatusType.ERROR
        else:
            if notify_type.group:
                collect_group_data.delay(new_notify.id)
            else:
                collect_person_data.delay(data, new_notify.id)
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
def collect_periodic_mailing():
    for mailing in Mailing.objects.filter(next_send__lte=timezone.now()):
        new_notify = Notify.objects.create(notify_type=mailing.notify_type)
        collect_group_data.delay(new_notify.id)


@app.task
def collect_person_data(data: dict, notify_id: int):
    """Собирает данные для персональной рассылки"""
    new_notify = Notify.objects.get(id=notify_id)
    new_notify.status = Notify.StatusType.SENDING
    new_notify.save()
    user_prefs = []
    for batch in get_user_prefs([data.get("user_id")], notify_id):
        user_prefs = batch[0].get("preferences")
        break
    providers = []
    user_data = get_user_data([data.get("user_id")], notify_id)[0]
    for notify_type in user_prefs:
        if notify_type.get("event_type") == data.get("notify_type"):
            providers.append(notify_type.get("provider"))
    for provider in providers:
        send_message.delay(
            notify_data=data,
            user_data=user_data,
            provider=provider,
            notify_id=notify_id,
        )


@app.task
def collect_group_data(notify_id: int):
    new_notify = Notify.objects.get(id=notify_id)
    new_notify.status = Notify.StatusType.SENDING
    new_notify.save()

    for user_data_batch in get_user_data(notify_id=notify_id):
        users_info = {user_data.get("id"): user_data for user_data in user_data_batch}
        user_ids = list(users_info.keys())

        for user_prefs_batch in get_user_prefs(user_ids, notify_id):
            for user_pref in user_prefs_batch:
                user_id = user_pref.get("user_id")
                preferences = user_pref.get("preferences")

                for notify_type in preferences:
                    if notify_type.get("event_type") != new_notify.notify_type.slug:
                        continue

                    send_message.delay(
                        notify_data=new_notify.content,
                        user_data=users_info.get(user_id),
                        provider=notify_type.get("provider"),
                        notify_id=notify_id,
                    )


@app.task
def retry_error_mailing():
    for notify in Notify.objects.filter(
        status=Notify.StatusType.ERROR,
        retry_count__lt=10,
        next_retry__lte=timezone.now(),
    ):
        notify.retry_count += 1
        notify.next_retry += timedelta(minutes=notify.retry_count * 2)
        notify.save()
        if notify.notify_type.group:
            # нет смысла сохранять данные с прошлой попытки, т.к они потеряют консистентность
            collect_group_data.delay(notify_id=notify.id)
        else:
            collect_person_data.delay(data=notify.content, notify_id=notify.id)


def get_user_prefs(user_ids: list, notify_id: int) -> Generator:
    new_notify = Notify.objects.get(id=notify_id)
    if (
        settings.USER_PREFERENCES_SERVICE_URL
        and settings.USER_PREFERENCES_SERVICE_TOKEN
    ):
        counter = 0
        limit = 50
        while counter < len(user_ids):
            url = (
                f"{settings.USER_PREFERENCES_SERVICE_URL}/preferences/api/v1/user-preferences/list"
                f"?only_with_events=True&user_ids={user_ids[counter:counter+limit-1]}"
            )
            counter += limit
            response = requests.get(
                url=url,
                headers={
                    "Authorization": "Bearer " + settings.USER_PREFERENCES_SERVICE_TOKEN
                },
            )
            if response.status_code == HTTPStatus.OK:
                yield response.json()
            else:
                new_notify.error_text = (
                    f"user-prefs: {response.status_code}: {response.text}"
                )
                new_notify.status = Notify.StatusType.ERROR
                new_notify.save()
                raise Exception(response.text)

    else:
        new_notify.error_text = f"Не задан адрес или токен сервиса настроек"
        new_notify.status = Notify.StatusType.ERROR
        new_notify.save()
        raise Exception("Не задан адрес или токен сервиса настроек")


def get_user_data(notify_id: int, user_id: list | None = None) -> Generator:
    new_notify = Notify.objects.get(id=notify_id)

    if settings.AUTH_SERVICE_URL and settings.AUTH_SERVICE_TOKEN:
        page_number = 1
        while True:
            url = f"{settings.AUTH_SERVICE_URL}/auth/api/v1/users/user-infos?page_number={page_number}&limit=50"
            if user_id:
                url += f"&user_ids={user_id}"
            else:
                url += f"&user_groups=[{new_notify.notify_type.auth_group}]"
            response = requests.get(
                url=url,
                headers={"Authorization": "Bearer " + settings.AUTH_SERVICE_TOKEN},
            )
            page_number += 1
            if response.status_code == HTTPStatus.OK:
                yield response.json().get("result")
            if not response.json().get("outcome")[0].get("next_page"):
                break
            else:
                new_notify.error_text = f"{response.status_code}: {response.text}"
                new_notify.status = Notify.StatusType.ERROR
                new_notify.save()
                break
    else:
        new_notify.error_text = f"Не задан адрес или токен сервиса авторизации"
        new_notify.status = Notify.StatusType.ERROR
        new_notify.save()
        raise Exception("Не задан адрес или токен сервиса авторизации")
