"""Модуль с вспомогательными объектами."""

from uuid import UUID
from collections import namedtuple

from django.http import HttpRequest

from .models import NotifyType

EventValidatorResponse = namedtuple('EventValidatorResponse', ['status', 'detail'])


class EventValidator:
    """Класс-валидатор для событий."""

    async def validate(self, request: HttpRequest) -> EventValidatorResponse:
        """Метод валидирует данные из `request`."""

        if not request.GET.get("event_type"):
            return EventValidatorResponse(status=False, detail='Не передан тип события!')

        if (event_type_data :=
                await NotifyType.objects.filter(slug__iexact=request.GET.get("event_type")).values().afirst()):

            if not event_type_data.get('group'):
                if request.GET.get("user_id"):
                    if not await self.is_uuid_valid(request.GET.get("user_id")):
                        return EventValidatorResponse(
                            status=False, detail='Параметр user_id должен быть в формате UUID!'
                        )
                    return EventValidatorResponse(status=True, detail='')
                return EventValidatorResponse(status=False, detail='Не передан идентификатор пользователя!')

            return EventValidatorResponse(status=True, detail='')

        return EventValidatorResponse(status=False, detail='Такого типа события не существует!')

    @staticmethod
    async def is_uuid_valid(obj: str) -> bool:
        """Метод проверяет является ли переданный объект UUID-ом."""

        try:
            UUID(obj)
        except ValueError:
            return False
        return True
