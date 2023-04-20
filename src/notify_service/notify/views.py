from django.http import JsonResponse, HttpRequest
import abc

from serializers import PersonalNotifySerializer
from tasks import treatment_api_data


class EventValidator(abc.ABC):
    def validate(self):
        pass


async def create_notify(request: HttpRequest):
    # валидация
    treatment_api_data.delay(data=request.POST)
    return JsonResponse(status=201)
