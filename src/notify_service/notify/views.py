"""Модуль с реализациями ручек  API Django."""

from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from .utils import EventValidator
from notify.models import NotifyType
from notify.tasks import treatment_api_data


@csrf_exempt
def create_notify(request: HttpRequest):
    """ Функция, принимающая данные для отправки уведомления и передающая их в `Celery task`."""

    validator = EventValidator()

    if validator.validate(request):
        # treatment_api_data.delay(data=request.GET)
        return HttpResponse('OK')

    return HttpResponseBadRequest('BadRequest')
