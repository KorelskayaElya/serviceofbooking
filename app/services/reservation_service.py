"""
Сервис работы с резервом столов: создание, удаление и получение.
"""
import logging
from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.reservation import Reservation
from app.schemas import reservation as reservation_schema

logger = logging.getLogger(__name__)


def get_all_reservations(db: Session):
    """
    Получает список всех бронирований из базы данных.
    """
    logger.info("Запрошен список всех бронирований.")
    return db.query(Reservation).all()


def create_reservation(db: Session, reservation: reservation_schema.ReservationCreate):
    """
    Создаёт новое бронирование, если столик свободен в заданный временной промежуток.
    """
    start_time = reservation.reservation_time
    end_time = start_time + timedelta(minutes=reservation.duration_minutes)
    logger.info("Попытка создать бронь: %s", reservation.model_dump())


    existing_reservations = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id
    ).all()

    for existing in existing_reservations:
        existing_end = existing.reservation_time + timedelta(minutes=existing.duration_minutes)
        if start_time < existing_end and end_time > existing.reservation_time:
            logger.warning("Конфликт при бронировании. Столик уже занят.")
            raise ValueError("Столик уже забронирован на это время")

    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    logger.info("Бронирование успешно создано: id=%d", db_reservation.id)

    return db_reservation


def delete_reservation(db: Session, reservation_id: int) -> bool:
    """
    Удаляет бронирование по ID, если оно существует.
    """
    logger.info("Попытка удалить бронь с ID %d", reservation_id)
    reservation = db.query(Reservation).get(reservation_id)
    if reservation:
        db.delete(reservation)
        db.commit()
        logger.info(f"Бронь удалена: id=%d{reservation_id}")
        return True
    logger.warning("Бронь не найдена для удаления: id=%d", reservation_id)
    return False