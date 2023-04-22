"""Модуль содержит фабрики для поисковиков."""
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient

from src.services.searchers.searchers import Searcher, MongoUserPreferencesSearcher
from src.services.types import TStorageClient


_USER_PREFERENCES_SEARCHERS = {
    AsyncIOMotorClient: MongoUserPreferencesSearcher,
}


@lru_cache()
def get_user_preferences_searcher_by_client(client: TStorageClient) -> Searcher:
    try:
        cls = _USER_PREFERENCES_SEARCHERS[type(client)]
        return cls(client)
    except KeyError:
        raise KeyError('Не задана реализация для клиента.')
