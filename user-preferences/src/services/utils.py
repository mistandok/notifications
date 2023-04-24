"""Модуль содержит различные утилиты."""
from enum import Enum
from typing import Any


def get_enum_values(enum: type(Enum)) -> list[Any]:
    """
    Получает все значения из перечисления

    Args:
        enum: Перечисление, из которого нужно получить значение.

    Returns:
        list
    """
    return [e.value for e in enum]
