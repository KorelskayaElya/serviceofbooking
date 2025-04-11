"""Модель SQLAlchemy для столиков (Table) в ресторане."""

from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Table(Base):
    """
    Модель столика в ресторане.

    Атрибуты:
        id (int): Уникальный идентификатор столика.
        name (str): Название столика (уникальное).
        seats (int): Количество посадочных мест.
        location (str): Расположение столика (например, "у окна").
    """

    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
