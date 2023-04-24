"""Модуль содержит модели для тел запросов."""
from pydantic import Field

from src.models.base import JSONModel
from src.models.user_preferences import Preferences


class UserPreferencesBody(JSONModel):
    """Класс описывает тело запроса для пользовательских предпочтений."""

    preferences: list[Preferences] = Field(default_factory=list)
