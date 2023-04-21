"""Модуль, отвечающий за интерфейсы CRUD действий."""
from abc import ABC
from typing import Any

from pydantic import BaseModel


class BaseCRUD(ABC):
    """Класс описывает интерфейс для CRUD операциц."""

    async def get(self, key_values: dict[str, Any]) -> BaseModel:
        """
        Метод находит значение по заданным ключевым значениям.

        Args:
            key_values: значения ключевых полей и их названия.

        Returns:
            BaseModel
        """
        raise NotImplementedError('Необходимо реализовать метод.')

    async def insert(self, object_for_insert: BaseModel) -> Any:
        """
        Метод создает новый объект.

        Args:
            object_for_insert: новый объект

        Returns:
            Идентификатор созданной записи.
        """
        raise NotImplementedError('Необходимо реализовать метод.')

    async def update(self, key_values: dict[str, Any], new_values: dict[str, Any]):
        """
        Метод обновляет существующий объект.

        Args:
            key_values: значения ключевых полей и их названия для поиска существующей записи.
            new_values: значения для новых полей и их названия.
        """
        raise NotImplementedError('Необходимо реализовать метод.')

    async def delete(self, key_values: dict[str, Any]):
        """
        Метод удаляет объект по ключу.

        Args:
            key_values: значения ключевых полей и их названия.
        """
        raise NotImplementedError('Необходимо реализовать метод.')
