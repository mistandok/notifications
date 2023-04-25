"""Модуль содержит настройки для работы FastApi-приложения."""

import os
from enum import Enum, StrEnum
from logging import config as logging_config
from functools import cached_property

from pydantic import BaseSettings, Field
from pathlib import Path

from .logger import LOGGING


BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG_ENV = os.path.join(BASE_DIR, 'core', '.env.prod.debug')
PROD_ENV = os.path.join(BASE_DIR, 'core', '.env.prod.prod')

project_env = PROD_ENV


class CollectionName(Enum):
    """Класс определяет название коллекций для работы с mongo"""

    USER_PREFERENCES = 'user_preferences'


class DatabaseName(Enum):
    """Класс определяет название баз данных для работы с mongo"""

    PREFERENCES = 'preferences'


class EventType(StrEnum):
    """Класс описывает доступные события."""

    AUTH = 'auth'
    TOP_FILM = 'top_film'


class ProviderType(StrEnum):
    """Класс описывает доступные провайдеры."""

    EMAIL = 'mail'


class UserRole(StrEnum):
    """Класс описывает пользовательские роли."""

    ADMIN = 'admin'


class Settings(BaseSettings):

    project_name: str = Field(..., env='PROJECT_NAME')
    project_version: str = Field(..., env='PROJECT_VERSION')

    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(..., env='REDIS_PORT')

    timeline_of_cache: int = Field(..., env='TIMELINE_OF_CACHE')

    debug: str = Field(..., env='DEBUG')

    class Config:
        keep_untouched = (cached_property,)
        env_file = project_env


class SearchersSettings(BaseSettings):
    """Класс настроек для поисковиков."""

    limit_for_search_user_preferences: int = Field(..., env='LIMIT_FOR_SEARCH_UP')

    class Config:
        env_file = project_env


class MongoDBSettings(BaseSettings):
    """Класс настроек для MongoDB"""

    mongos1_host: str = Field(..., env='MONGOS1_HOST')
    mongos1_port: int = Field(..., env='MONGOS1_PORT')

    mongos2_host: str = Field(..., env='MONGOS2_HOST')
    mongos2_port: int = Field(..., env='MONGOS2_PORT')

    db_name: str = Field(..., env='MONGO_DATABASE')
    timeout_ms: int = Field(..., env='MONGO_TIMEOUT_MS')

    class Config:
        env_file = project_env


class JWTSettings(BaseSettings):
    """Класс настроек для JWT-токенов"""

    secret_key: str = Field(..., env='JWT_SECRET_KEY')
    algorithm: str = Field(..., env='JWT_ALGORITHM')

    class Config:
        env_file = project_env


settings = Settings()
mongodb_settings = MongoDBSettings()
jwt_settings = JWTSettings()
searchers_settings = SearchersSettings()

logging_config.dictConfig(LOGGING)
