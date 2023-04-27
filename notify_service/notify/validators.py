"""Модуль с вспомогательными объектами."""

from uuid import UUID

from django.http import HttpRequest

from .models import NotifyType


class EventValidator:
    """Класс-валидатор для событий."""

    async def validate(self, request: HttpRequest) -> str:
        """Метод валидирует данные из `request`."""

        if not request.GET.get("event_type"):
            return 'Не передан тип события!'

        if (event_type_data :=
                await NotifyType.objects.filter(slug__iexact=request.GET.get("event_type")).values().afirst()):

            if not event_type_data.get('group'):
                if request.GET.get("user_id"):
                    if not await self.is_uuid_valid(request.GET.get("user_id")):
                        return 'Параметр user_id должен быть в формате UUID!'
                    return 'OK'
                return 'Не передан идентификатор пользователя!'

            return 'OK'

        return 'Такого типа события не существует!'

    @staticmethod
    async def is_uuid_valid(obj: str) -> bool:
        """Метод проверяет является ли переданный объект UUID-ом."""

        try:
            UUID(obj)
        except ValueError:
            return False
        return True
