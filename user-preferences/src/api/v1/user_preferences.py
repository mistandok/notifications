"""Модуль содерижт API для сервиса user-preferences."""
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.models.auth_models import HTTPTokenAuthorizationCredentials
from src.models.requests_body_models import UserPreferencesBody
from src.models.response_models import IdResponse, Response
from src.models.user_preferences import UserPreferences
from src.services.auth_validation.bearer_tokens import JWTBearer
from src.services.user_preferences import UserPreferencesService, get_user_preferences_service

user_preferences_router = APIRouter()

jwt_bearer = JWTBearer()


@user_preferences_router.post(
    '/upsert',
    response_model=IdResponse,
    summary='Добавление пользовательских предпочтений для конкретного пользователя.',
    response_description='Идентификатор записи.',
    description='',
)
async def upsert_user_preferences(
    body: UserPreferencesBody,
    user_preferences_service: UserPreferencesService = Depends(get_user_preferences_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
):
    """
    Ручка позволяет пользователю создавать, добавлять или изменять пользовательские предпочтения.

    Args:
        body: тело запроса.
        user_preferences_service: сервис пользовательских предпочтений.
        credentials: данные входа
    """
    user_id = credentials.payload.sub.user_id
    return await user_preferences_service.upsert_user_preferences(
        user_id=user_id,
        preferences=body.preferences,
    )


@user_preferences_router.patch(
    '/drop-preferences',
    response_model=Response,
    summary='Удаляет заданные пользовательские уведомления.',
    response_description='Сообщение.',
    description='',
)
async def drop_custom_user_preference(
    body: UserPreferencesBody,
    user_preferences_service: UserPreferencesService = Depends(get_user_preferences_service),
    credentials: HTTPTokenAuthorizationCredentials = Depends(jwt_bearer),
):
    user_id = credentials.payload.sub.user_id
    await user_preferences_service.drop_custom_user_preference(
        user_id=user_id,
        preferences=body.preferences,
    )
    return Response(detail='Заданные пользовательские настройки успешно удалены!')


@user_preferences_router.get(
    '/list',
    response_model=list[UserPreferences],
    summary='Предоставление списка пользовательских предпочтений',
    response_description='Список пользовательских предпочтений.',
    description=''
)
async def get_user_preferences_list(
    user_ids: list[UUID | str] = Query(),
    only_with_events: bool = Query(default=False),
    user_preferences_service: UserPreferencesService = Depends(get_user_preferences_service),
) -> list[UserPreferences]:
    """
    Ручка позволяет получить информацию по предпочтениям для заданных пользовательских идентификаторов.

    Args:
        user_ids: список пользователей, по которым необходимо получить информацию. Не более 1000 пользователей за раз.
        only_with_events: показывать только тех пользователей, которые подписаны хотябы на одно уведомление.
        user_preferences_service: сервис для рпбоы с пользовательскими предпочтениями.
    """
    return await user_preferences_service.get_user_preferences_list(user_ids, only_with_events)
