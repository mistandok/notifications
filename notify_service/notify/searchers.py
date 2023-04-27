"""Модуль содержит различные функции и объекты для поиска данных."""
from http import HTTPStatus
from typing import Generator

import requests

from config import settings
from notify.models import Notify


def get_personal_user_prefs(user_id: str, notify_id: int) -> dict:
    """
    Функция получает пользовательские предпочтения для конретного пользователя.
    @param user_id: id пользователей
    @param notify_id: id уведомления
    """
    user_prefs_batch = next(get_user_prefs([user_id], notify_id))
    try:
        return user_prefs_batch[0].get('preferences')
    except IndexError:
        raise Exception('Не удалось найти никаких пользовательских предпочтений по пользователю.')


def get_personal_user_data(user_id: str, notify_id: int) -> dict:
    """
    Функция получает пользовательские данные для конретного пользователя.
    @param user_id: id пользователей
    @param notify_id: id уведомления
    """
    user_data_batch = next(get_user_data(notify_id, [user_id]))
    try:
        return user_data_batch[0]
    except IndexError:
        raise Exception('Не удалось найти никаких данных по пользователю.')


def get_user_prefs(user_ids: list, notify_id: int) -> Generator:
    """
    Сбор данных из сервиса настроек
    @param user_ids: id пользователей
    @param notify_id: id уведомления
    """
    new_notify = Notify.objects.get(id=notify_id)

    if not all((settings.AUTH_SERVICE_URL, settings.AUTH_SERVICE_TOKEN)):
        new_notify.error_text = "Не задан адрес или токен сервиса настроек"
        new_notify.status = Notify.StatusType.ERROR
        new_notify.save()
        raise Exception("Не задан адрес или токен сервиса настроек")

    counter = 0
    limit = 50

    while counter < len(user_ids):
        url = (
            f"{settings.USER_PREFERENCES_SERVICE_URL}/preferences/api/v1/user-preferences/list"
            f"?only_with_events=True"
        )

        current_users_slice = slice(counter, counter + limit - 1)
        url += ''.join((f"&user_ids={user_id}" for user_id in user_ids[current_users_slice]))

        counter += limit
        response = requests.get(
            url=url,
            headers={
                "Authorization": "Bearer " + settings.USER_PREFERENCES_SERVICE_TOKEN
            },
        )

        if response.status_code == HTTPStatus.OK:
            response_json = response.json()

            if not len(response_json):
                new_notify.error_text = "Нету данных из сервиса настроек"
                new_notify.status = Notify.StatusType.ERROR
                new_notify.save()
                raise Exception("Нету данных из сервиса настроек")

            yield response.json()
        else:
            new_notify.error_text = (
                f"user-prefs: {response.status_code}: {response.text}"
            )
            new_notify.status = Notify.StatusType.ERROR
            new_notify.save()
            raise Exception(f"user-prefs: {response.status_code}: {response.text}: {url}")


def get_user_data(notify_id: int, user_ids: list | None = None) -> Generator:
    """
    Собирает данные из сервиса авторизации
    @param user_ids: id пользователей
    @param notify_id: id уведомления
    """
    new_notify = Notify.objects.get(id=notify_id)

    if not all((settings.AUTH_SERVICE_URL, settings.AUTH_SERVICE_TOKEN)):
        new_notify.error_text = "Не задан адрес или токен сервиса настроек"
        new_notify.status = Notify.StatusType.ERROR
        new_notify.save()
        raise Exception("Не задан адрес или токен сервиса настроек")

    page_number = 1

    while True:
        url = f"{settings.AUTH_SERVICE_URL}/auth/api/v1/users/user-infos?page_number={page_number}&limit=50"

        if user_ids:
            url += ''.join((f"&user_ids={user_id}" for user_id in user_ids))
        elif new_notify.notify_type.auth_group:
            url += f"&user_groups={new_notify.notify_type.auth_group}"

        response = requests.get(
            url=url,
            headers={"Authorization": "Bearer " + settings.AUTH_SERVICE_TOKEN},
        )

        page_number += 1

        if response.status_code == HTTPStatus.OK:
            response_json = response.json()

            if not response_json.get("result"):
                new_notify.error_text = "Нету данных из сервиса авторизации"
                new_notify.status = Notify.StatusType.ERROR
                new_notify.save()
                raise Exception("Нету данных из сервиса авторизации")

            yield response_json.get("result")

            if not response_json.get("outcome")[0].get("next_page"):
                break
        else:
            new_notify.error_text = f"auth: {response.status_code}: {response.text} : {url}"
            new_notify.status = Notify.StatusType.ERROR
            new_notify.save()
            raise Exception(f"auth: {response.status_code}: {response.text}: {url}")
