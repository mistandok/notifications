"""Модуль содержит сервис для работы с user_preferences."""

from functools import lru_cache

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from src.core.config import DatabaseName, CollectionName
from src.db.mongodb import get_mongo_client
from src.db.redis import get_redis
from src.models.response_models import IdResponse
from src.models.user_preferences import UserPreferences, Preferences
from src.services.crud.factories import get_crud_object_by_client
from src.services.types import TStorageClient, CacheClient


class UserPreferencesService:
    """
    Класс отвечает за доступные действия с пользовательскими предпочтениями

    Attributes:
        cache_client: клиент кэша.
        _storage_client: клиент для работы с хранилищем данных.
        _user_preferences: объект для CRUD-операций с хранилищем данных.
    """

    __slots__ = ('cache_client', '_storage_client', '_user_preferences')

    def __init__(self, storage_client: TStorageClient, cache_client: CacheClient):
        self.cache_client = cache_client
        self._storage_client = storage_client
        self._user_preferences = get_crud_object_by_client(
            storage_client,
            db_name=DatabaseName.PREFERENCES.value,
            collection_name=CollectionName.USER_PREFERENCES.value,
            model=UserPreferences,
        )

    async def upsert_user_preferences(self, user_id: str, preferences: list[Preferences]) -> IdResponse:
        """
        Метод добавляет пользовательские настройки для пользователя.

        Args:
            user_id: идентификатор пользователя.
            preferences: пользовательские предпочтения.
        """
        user_preferences = await self._user_preferences.get(dict(user_id=user_id))

        if user_preferences:
            current_preferences = user_preferences.preferences

            is_need_update = False
            for new_preference in preferences:
                if new_preference not in current_preferences:
                    current_preferences.append(new_preference)
                    is_need_update = True

            if is_need_update:
                encoded_preferences = [jsonable_encoder(preference) for preference in current_preferences]
                await self._user_preferences.update(dict(user_id=user_id), dict(preferences=encoded_preferences))

            result_id = str(user_preferences.id)
        else:
            new_user_preferences = UserPreferences(user_id=user_id, preferences=preferences)
            result_id = await self._user_preferences.insert(new_user_preferences)

        return IdResponse(id=result_id)


@lru_cache()
def get_user_preferences_service(
        storage_client: TStorageClient = Depends(get_mongo_client),
        cache_client: CacheClient = Depends(get_redis),
) -> UserPreferencesService:
    """
    Функция возвращает сервис для работы с пользовательскими предпочтениями.

    Args:
        storage_client: клиент для работы с хранилищем данных.
        cache_client: клиент кэша.

    Returns:
        UserPreferencesService
    """
    return UserPreferencesService(storage_client, cache_client)
