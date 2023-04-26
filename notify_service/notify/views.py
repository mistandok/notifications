"""Модуль с реализациями ручек  API Django."""

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseBase

from .utils import EventValidator
from notify.tasks import treatment_api_data


async def create_notify(request: HttpRequest) -> HttpResponseBase:
    """ Функция, принимающая данные для отправки уведомления и передающая их в `Celery task`."""

    validator = EventValidator()

    if (validate_result := await validator.validate(request)) == 'OK':
        # treatment_api_data.delay(data=request.GET)
        return HttpResponse(validate_result)

    return HttpResponseBadRequest(validate_result)
