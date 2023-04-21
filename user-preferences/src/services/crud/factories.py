"""Модуль содержит фабрики для предоставления CRUD-объектов."""
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient

from src.services.types import TStorageClient
from src.services.crud.mongo_realisation import MongoCRUD
from src.services.crud.interfaces import BaseCRUD


_CRUD_MAP = {
    AsyncIOMotorClient: MongoCRUD,
}


@lru_cache()
def get_crud_object_by_client(client: TStorageClient, *args, **kwargs) -> BaseCRUD:
    try:
        cls = _CRUD_MAP[type(client)]
        return cls(client, *args, **kwargs)
    except KeyError:
        raise KeyError('Не задана реализация для клиента.')
