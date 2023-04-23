"""Модуль содержит различные поисковики специализированной информации по пользовательскому рейтингу фильмов."""
from abc import ABC
from http import HTTPStatus
from typing import Any

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.core.config import DatabaseName, CollectionName, searchers_settings

from src.models.user_preferences import UserPreferences


class Searcher(ABC):
    """Базовый интерфей для поиска"""

    async def get(self, *args, **kwargs) -> Any:
        """
        Метод осуществляет поиск информации в зависимости от конкретной реализации.

        Args:
            args: позиционные параметры.
            kwargs: именнованые параметры.

        Returns:
            Any
        """
        raise NotImplementedError('Необходимо реализовать метод интерфейса!')


class MongoUserPreferencesSearcher(Searcher):
    """Класс отвечает за поиск среднего рейтинга фильма в MongoDB"""

    def __init__(self, client: AsyncIOMotorClient):
        self._client = client
        self._database: AsyncIOMotorDatabase = self._client[DatabaseName.PREFERENCES.value]
        self._collection: AsyncIOMotorCollection = self._database[CollectionName.USER_PREFERENCES.value]
        self._limit = searchers_settings.limit_for_search_user_preferences

    async def get(self, user_ids: list[str], only_with_events: bool = False) -> list[UserPreferences]:
        """
        Метод осуществляет поиск пользовательских настроек пользователей по идентификаторам.

        Args:
            user_ids: идентификатор фильма.
            only_with_events: только пользователь с подпиской хотя бы на одно событие.

        Returns:
            list[UserPreferences]
        """
        if len(user_ids) > self._limit:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Максимальное количество идентификаторов для поиска {self._limit}',
            )

        if only_with_events:
            match = {
                '$match': {
                    '$and': [
                        {
                            '$expr': {
                                '$in': ['$user_id', [str(user_id) for user_id in user_ids]],
                            },
                        },
                        {
                            'preferences': {
                                '$ne': [],
                            },
                        },
                    ],
                },
            }
        else:
            match = {
                '$match': {
                    '$expr': {
                        '$in': ['$user_id', [str(user_id) for user_id in user_ids]],
                    },
                },
            }

        pipeline = [match]

        cursor = self._collection.aggregate(pipeline)
        user_preferences = await cursor.to_list(length=self._limit)

        return [UserPreferences(**user_preference) for user_preference in user_preferences]
