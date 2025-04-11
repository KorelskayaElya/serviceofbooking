"""Схемы (Pydantic-модели) для работы с данными бронирований (reservations)."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ReservationBase(BaseModel):
    """
    Базовая схема бронирования.

    Содержит общие поля, используемые при создании и отображении бронирования.
    """
    customer_name: str # Имя клиента
    table_id: int # ID столика
    reservation_time: datetime  # Время начала бронирования
    duration_minutes: int # Продолжительность бронирования в минутах


class ReservationCreate(ReservationBase):
    """
    Схема для создания бронирования.

    Наследуется от ReservationBase. Используется при создании записи.
    """
    pass


class ReservationRead(ReservationBase):
    """
    Схема для чтения (вывода) данных бронирования.
    """
    id: int

    model_config = ConfigDict(from_attributes=True)
