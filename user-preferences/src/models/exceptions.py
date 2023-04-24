"""Модуль описывает базовые модели данных ошибок, которые могут быть возвращены."""

from pydantic import BaseModel


class ExceptionResponse(BaseModel):
    """Результат метода для Ошибок."""

    msg: str
    status_code: str
