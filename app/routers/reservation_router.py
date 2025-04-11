"""Роутер для операций с бронированиями (reservations)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import reservation as reservation_schema
from app.services import reservation_service
from app.database.session import SessionLocal

router = APIRouter()


def get_db():
    """
    Создаёт и возвращает сессию базы данных.
    После завершения запроса сессия автоматически закрывается.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[reservation_schema.ReservationRead])
def read_reservations(db: Session = Depends(get_db)):
    """
    Получить список всех бронирований.

    :param db: Сессия базы данных
    :return: Список объектов ReservationRead
    """
    return reservation_service.get_all_reservations(db)


@router.post("/", response_model=reservation_schema.ReservationRead)
def create_reservation(
    reservation: reservation_schema.ReservationCreate,
    db: Session = Depends(get_db)
    ):
    """
    Создать новое бронирование.

    :param reservation: Данные нового бронирования
    :param db: Сессия базы данных
    :return: Объект ReservationRead
    :raises HTTPException: Если есть пересечение по времени с другим бронированием
    """
    try:
        return reservation_service.create_reservation(db, reservation)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


@router.delete("/{reservation_id}", status_code=204)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Удалить бронирование по ID.

    :param reservation_id: ID бронирования
    :param db: Сессия базы данных
    :raises HTTPException: Если бронирование не найдено
    """
    if not reservation_service.delete_reservation(db, reservation_id):
        raise HTTPException(status_code=404, detail="Reservation not found")
