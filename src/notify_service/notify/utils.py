"""Модуль с вспомогательными объектами."""
import abc
from uuid import UUID

from asgiref.sync import sync_to_async
from django.http import HttpRequest
from django.http.request import QueryDict

from .models import NotifyType


class EventValidator:
    """Класс-валидатор для событий."""
    def validate(self, request: HttpRequest) -> bool:
        """Метод валидирует данные из `request`."""

        if not self._have_params(request.GET):
            return False

        if NotifyType.objects.filter(slug__iexact=request.GET.get("event_type")).first():

            if request.GET.get("group") == 'False':
                if not self.is_uuid_valid(request.GET.get("user_id")):
                    return False

            return True

        else:
            return False

    @staticmethod
    def is_uuid_valid(obj: str) -> bool:
        """Метод проверяет является ли переданный объект UUID-ом."""

        try:
            UUID(obj)
        except ValueError:
            return False
        return True

    @staticmethod
    def _have_params(request_data: QueryDict) -> bool:
        """Метод проверяет есть ли нужные параметры в `request`."""

        if (request_data.get('event_type') and request_data.get('user_id')
                and request_data.get('group') in ('True', 'False')):
            return True
        return False
