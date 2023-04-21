"""Модуль содержит в себе модели для описания сущности film_review."""
from typing import Optional

from pydantic import Field

from src.models.base import MongoJSONModel, PyObjectId, JSONModel


class Preferences(JSONModel):
    """Класс описывает модель предпочтений пользователя."""

    event_type: str
    provider: str


class UserPreferences(MongoJSONModel):
    """Класс описывает модель сущности film_rating."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: str = Field(...)
    preferences: Optional[list[Preferences]] = Field(default_factory=list)
