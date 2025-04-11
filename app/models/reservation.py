"""Модель SQLAlchemy для бронирований (Reservation) столиков в ресторане."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database.base import Base


class Reservation(Base):
    """
    Модель бронирования столика.

    Атрибуты:
        id (int): Уникальный идентификатор брони.
        customer_name (str): Имя клиента, сделавшего бронирование.
        table_id (int): Внешний ключ на столик.
        reservation_time (datetime): Дата и время начала бронирования.
        duration_minutes (int): Продолжительность бронирования в минутах. Ограничения по времени нет.
    """

    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete="CASCADE"), nullable=False)
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
