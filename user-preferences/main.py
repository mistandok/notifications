"""Модуль, запускающий `uvicorn` сервер для FastApi-приложения."""

import uvicorn
import aioredis
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from src.api.v1.user_preferences import user_preferences_router
from src.core.config import settings, mongodb_settings
from src.db import redis
from src.db import mongodb

description = """
### API записи событий и контента пользователей.<br>
"""

app = FastAPI(
    title=settings.project_name,
    version=settings.project_version,
    description=description,
    contact={
        "name_1": "Антон",
        "url_1": "https://github.com/mistandok",
        "name_2": "Михаил",
        "url_2": "https://github.com/Mikhail-Kushnerev",
        "name_3": "Евгений",
        "url_3": "https://github.com/ME-progr"
    },
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    """Метод создает соединения при старте сервера."""
    redis.redis = await aioredis.create_redis_pool(
        (settings.redis_host, settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    mongodb.mongo_client = AsyncIOMotorClient(
        host=[
            f'{mongodb_settings.mongos1_host}:{mongodb_settings.mongos1_port}',
            f'{mongodb_settings.mongos2_host}:{mongodb_settings.mongos2_port}',
        ],
        serverSelectionTimeoutMS=mongodb_settings.timeout_ms,
    )


@app.on_event('shutdown')
async def shutdown():
    """Метод разрывает соединения при отключении сервера."""

    mongodb.mongo_client.close()
    redis.redis.close()
    await redis.redis.wait_closed()


app.include_router(user_preferences_router, prefix='/preferences/api/v1/user-preferences', tags=['rating'])


if __name__ == '__main__':

    if settings.debug.lower() == 'true':
        uvicorn.run(
            'main:app',
            host='0.0.0.0',
            port=8101,
        )
