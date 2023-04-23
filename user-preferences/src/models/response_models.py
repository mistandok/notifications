"""Модуль содержит модели, которые могут пригодиться в качестве ответа ручки."""
from pydantic import BaseModel

from src.models.base import MongoJSONModel, JSONModel
from src.models.user_preferences import UserPreferences


class Response(JSONModel):
    """Базовый ответ ручки."""

    detail: str


class IdResponse(JSONModel):
    """Класс описывает тело ответа, содержащее id записи."""

    id: str


class ListOutcome(MongoJSONModel):
    """Класс описывает outcome для списковых методов."""

    next_page: int | None = None


class ListResponse(MongoJSONModel):
    """Класс описывает стандартный ответ для списковых методов"""

    result: list[BaseModel]
    outcome: ListOutcome


class UserPreferencesListResponse(MongoJSONModel):
    """Класс описывает ответ для спискового метода отзывов по фильму"""

    result: list[UserPreferences]
    outcome: ListOutcome
