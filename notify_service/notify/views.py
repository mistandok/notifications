from django.http import JsonResponse, HttpRequest
import abc

from notify.models import NotifyType
from notify.tasks import treatment_api_data


class EventValidator(abc.ABC):
    def validate(self, request: HttpRequest) -> bool:
        if notify_type := NotifyType.objects.filter(slug__iexact=request.POST.get("event_type")).afirst():
            return True
        else:
            return False


async def create_notify(request: HttpRequest):
    validator = EventValidator()
    if validator.validate(request):
        treatment_api_data.delay(data=request.POST)
        return JsonResponse(data={}, status=201)
    else:
        return JsonResponse(data={}, status=400)
