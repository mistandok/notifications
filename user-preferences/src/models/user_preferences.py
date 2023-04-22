"""Модуль содержит в себе модели для описания сущности film_review."""
import datetime
from typing import Optional

from pydantic import Field, validator

from src.core.config import EventType, ProviderType
from src.models.base import MongoJSONModel, PyObjectId, JSONModel
from src.services.utils import get_enum_values


class Preferences(JSONModel):
    """Класс описывает модель предпочтений пользователя."""

    event_type: str
    provider: str

    @validator('event_type', each_item=True)
    def check_event_type_name(cls, value):
        enum_values = get_enum_values(EventType)
        if value not in enum_values:
            raise ValueError(f'Некорректное событие! поддерживаемые события: {enum_values}')
        return value

    @validator('provider', each_item=True)
    def check_provider_type_name(cls, value):
        enum_values = get_enum_values(ProviderType)
        if value not in enum_values:
            raise ValueError(f'Некорректный провайдер! поддерживаемые провайдеры: {enum_values}')
        return value


class UserPreferences(MongoJSONModel):
    """Класс описывает модель сущности film_rating."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    user_id: str = Field(...)
    preferences: Optional[list[Preferences]] = Field(default_factory=list)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
