"""Модуль содержит реализацию CRUD-интерфейса для работы с MongoDB."""
from http import HTTPStatus
from typing import Any

import pymongo.errors
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.models.base import MongoJSONModel
from src.services.crud.interfaces import BaseCRUD


class MongoCRUD(BaseCRUD):
    """Класс реализовывает CRUD-методы для MongoDB."""

    __slots__ = ('_client', '_database', '_collection', '_model')

    def __init__(self, client: AsyncIOMotorClient, db_name: str, collection_name: str, model: type(MongoJSONModel)):
        self._client = client
        self._database: AsyncIOMotorDatabase = self._client[db_name]
        self._collection: AsyncIOMotorCollection = self._database[collection_name]
        self._model = model

    async def get(self, key_values: dict[str, Any]) -> MongoJSONModel | None:
        """
        Метод находит значение по заданным ключевым значениям.

        Args:
            key_values: значения ключевых полей и их названия.

        Returns:
            BaseModel
        """
        result = await self._collection.find_one(key_values)
        return self._model(**result) if result else None

    async def insert(self, object_for_insert: MongoJSONModel) -> str:
        """
        Метод создает новый объект.

        Args:
            object_for_insert: новый пользовательский рейтинг для фильма.
        """
        new_object = jsonable_encoder(object_for_insert)
        try:
            insert_one_result = await self._collection.insert_one(new_object)
        except pymongo.errors.DuplicateKeyError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Сущность уже существует!')
        return insert_one_result.inserted_id

    async def update(self, key_values: dict[str, Any], new_values: dict[str, Any]):
        """
        Метод обновляет объект в коллекции.

        Args:
            key_values: значения ключевых полей и их названия.
            new_values: значения для новых полей и их названия.
        """
        try:
            await self._collection.update_one(key_values, {'$set': new_values})
        except pymongo.errors.DuplicateKeyError:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Сущность c такими параметрами уже есть!')

    async def delete(self, key_values: dict[str, Any]):
        """
        Метод удаляет объект в коллекции по ключу.

        Args:
            key_values: значения ключевых полей и их названия.
        """
        delete_one_result = await self._collection.delete_one(key_values)

        if not delete_one_result.deleted_count:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Сущность не существовала!')
