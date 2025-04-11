"""Роутер для операций со столами (tables)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import table as table_schema
from app.services import table_service
from app.database.session import SessionLocal

router = APIRouter()


def get_db():
    """
    Создаёт сессию базы данных и автоматически её закрывает после завершения запроса.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/", response_model=list[table_schema.TableCreate])
def read_tables(db: Session = Depends(get_db)):
    """
    Получить список всех столов из базы данных.

    :param db: Сессия базы данных
    :return: Список столов
    """
    return table_service.get_all_tables(db)



@router.post("/", response_model=table_schema.TableRead)
def create_table(table: table_schema.TableCreate, db: Session = Depends(get_db)):
    """
    Создать новый стол.

    :param table: Данные нового стола
    :param db: Сессия базы данных
    :return: Созданный стол
    """
    return table_service.create_table(db, table)



@router.delete("/{table_id}", status_code=204)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    """
    Удалить стол по ID.

    :param table_id: ID стола
    :param db: Сессия базы данных
    :raises HTTPException: если стол не найден
    """
    if not table_service.delete_table(db, table_id):
        raise HTTPException(status_code=404, detail="Table not found")
