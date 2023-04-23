"""Базовая Pydantic-схема для классов наследников."""
import orjson
from bson import ObjectId
from pydantic import BaseModel


def orjson_dumps(obj, *, default):
    """
    Метод ускоряет работу с JSON

    Args:
        obj (Any): Объект для представления в словарь
        default (Callable): Функция для сериализации.

    Returns: unicode

    """
    return orjson.dumps(obj, default=default).decode()


class JSONModel(BaseModel):
    """Класс, добавляющий конфигурацию для работы с json-объектами."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class MongoJSONModel(BaseModel):
    """Кдасс являющийся базовым для всех моделей, связанных с mongodb."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
