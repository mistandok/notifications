"""Модуль с вспомогательными объектами."""

from uuid import UUID

from django.http import HttpRequest
from django.http.request import QueryDict

from .models import NotifyType


class EventValidator:
    """Класс-валидатор для событий."""

    async def validate(self, request: HttpRequest) -> bool:
        """Метод валидирует данные из `request`."""

        if not await self._have_params(request.GET):
            return False

        if await NotifyType.objects.filter(slug__iexact=request.GET.get("event_type")).afirst():
            if request.GET.get("group") == 'False' and not await self.is_uuid_valid(request.GET.get("user_id")):
                return False

            return True
        return False

    @staticmethod
    async def is_uuid_valid(obj: str) -> bool:
        """Метод проверяет является ли переданный объект UUID-ом."""

        try:
            UUID(obj)
        except ValueError:
            return False
        return True

    @staticmethod
    async def _have_params(request_data: QueryDict) -> bool:
        """Метод проверяет есть ли нужные параметры в `request`."""

        if request_data.get('event_type') and request_data.get('group') in ('True', 'False'):
            if request_data.get('group') == 'False' and not request_data.get('user_id'):
                return False

            return True
        return False
