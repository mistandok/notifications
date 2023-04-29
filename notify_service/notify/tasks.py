from datetime import timedelta

from django.utils import timezone

from config.celery import app
from notify.models import Notify, NotifyType, Mailing
from notify.providers.provider import get_sender_by_provider
from notify.searchers import (
    get_personal_user_prefs,
    get_personal_user_data,
    get_user_data,
    get_user_prefs,
)


@app.task
def treatment_api_data(data: dict):
    """Обрабатывает данные от апи
    @param data: тело запроса, которое передается для рендера сообщения (вообще без разницы, что там будет,
    главное нужны notify_type и user_id)
    """
    new_notify: Notify = Notify.objects.create(content=data)
    if notify_type := NotifyType.objects.filter(slug=data.get("event_type")).first():
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
def send_message(users_data: list, provider: str, notify_id: int):
    """
    Выбирает провайдера и отправляет уведомление через него.
    @param users_data: данные пользователя формата
        [
          {'email': 'bexram33@mail.ru',
           'surname': 'Ilya',
           ...},
        ...]
    @param provider: провайдер для отправки
    @param notify_id: id уведомления
    """
    new_notify = Notify.objects.get(id=notify_id)
    try:
        sender = get_sender_by_provider(provider)
        sender.send(users_data, new_notify)
    except Exception as e:
        error_text = "Ошибка на стороне сервиса отправки сообщений: " + str(e)
        new_notify.error_text = error_text
        new_notify.status = Notify.StatusType.ERROR
        new_notify.save()
    else:
        new_notify.status = Notify.StatusType.SENDED
        new_notify.save()


@app.task
def collect_periodic_mailing():
    for mailing in Mailing.objects.filter(next_send__lte=timezone.now()):
        new_notify = Notify.objects.create(notify_type=mailing.notify_type)
        collect_group_data.delay(new_notify.id)


@app.task
def collect_person_data(data: dict, notify_id: int):
    """
    Собирает данные для персональной рассылки.
    @param data: данные для сбора
    @param notify_id: id уведомления
    """
    new_notify = Notify.objects.get(id=notify_id)
    new_notify.status = Notify.StatusType.SENDING
    new_notify.save()

    current_user_id = data.get("user_id")
    current_event_type = data.get("event_type")

    user_prefs = get_personal_user_prefs(current_user_id, notify_id)
    providers = [
        pref.get("provider")
        for pref in user_prefs
        if pref.get("event_type") == current_event_type
    ]
    if providers:
        user_data = get_personal_user_data(current_user_id, notify_id)
        for provider in providers:
            send_message.delay(
                users_data=[user_data], provider=provider, notify_id=new_notify.id
            )


@app.task
def collect_group_data(notify_id: int):
    """
    Собирает данные для групповой рассылки
    @param notify_id: id уведомления
    """
    new_notify = Notify.objects.get(id=notify_id)
    new_notify.status = Notify.StatusType.SENDING
    new_notify.save()
    messages_data = {}
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
                    if notify_type.get("provider") not in messages_data:
                        messages_data[notify_type.get("provider")] = [
                            users_info.get(user_id)
                        ]
                    else:
                        messages_data[notify_type.get("provider")].append(
                            users_info.get(user_id)
                        )
    for provider in messages_data.keys():
        send_message.delay(
            user_data=messages_data[provider],
            provider=provider,
            notify_id=notify_id,
        )


@app.task
def retry_error_mailing():
    """
    Собирает ошибочные таски для повторной отправки
    """
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
