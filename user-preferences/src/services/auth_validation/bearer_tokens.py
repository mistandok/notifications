"""Модуль отвечает за функционал, позволяющий обрабатывать поступающий из запросов токены и валидировать их."""
from http import HTTPStatus

import jwt

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.core.config import jwt_settings, UserRole
from src.models.auth_models import HTTPTokenAuthorizationCredentials, AccessTokenPayload


class JWTBearer(HTTPBearer):
    """Класс производит валидацию поступившего от клиента токена."""

    def __init__(self, *args, admin_required: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self._admin_required = admin_required

    async def __call__(self, request: Request):
        """
        Метод осуществляет проверку авторизационных данных клиента.

        Args:
            request: запрос.

        Returns:
            HTTPTokenAuthorizationCredentials
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        scheme, encoded_token = credentials.scheme, credentials.credentials
        token_payload = try_get_token_payload(encoded_token)

        credentials = HTTPTokenAuthorizationCredentials(scheme=scheme, payload=token_payload)

        if self._admin_required:
            user_roles = credentials.payload.sub.user_roles
            if UserRole.ADMIN.value not in user_roles:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Admin required.")

        return credentials


def try_get_token_payload(encoded_token: str) -> AccessTokenPayload:
    """
    Функция пытается расшифровать токени получить из него информацию.

    Args:
        encoded_token: зашифрованный токен.

    Returns:
        расшифрованый токен.
    """
    try:
        return jwt.decode(
            encoded_token,
            jwt_settings.secret_key.encode('utf-8'),
            algorithms=[jwt_settings.algorithm],
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid or expired token.")
