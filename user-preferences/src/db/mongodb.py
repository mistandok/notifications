"""Модуль, дающий возможность работать с MongoDB."""

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.core.config import mongodb_settings

mongo_client: AsyncIOMotorClient | None = None


async def get_mongo_client() -> AsyncIOMotorClient:
    """
    Метод-провайдер, дающий по заданному соединению объект класса AsyncIOMotorClient.

    Returns: AsyncIOMotorClient.
    """
    return mongo_client


async def get_mongo_database(client: AsyncIOMotorClient = Depends(get_mongo_client)) -> AsyncIOMotorDatabase:
    """
    Метод-провайдер, дающий по заданному соединению объект класса AsyncIOMotorDatabase.

    Returns: AsyncIOMotorDatabase.
    """
    return client[mongodb_settings.db_name]
