"""Схемы (Pydantic-модели) для работы с данными столиков в ресторане."""

from pydantic import BaseModel, ConfigDict


class TableBase(BaseModel):
    """Базовая схема столика с основными полями."""
    name: str  # Название столика
    seats: int # Количество посадочных мест
    location: str # Расположение в зале (например, "у окна")


class TableCreate(TableBase):
    """
    Схема создания нового столика.

    Наследует поля из TableBase.
    Используется при получении данных от пользователя.
    """
    pass


class TableRead(TableBase):
    """
    Схема чтения (возврата) столика из БД.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)