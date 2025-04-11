"""
Сервис работы со столами: создание, удаление и получение.
"""
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.table import Table
from app.schemas import table as table_schema

logger = logging.getLogger(__name__)


def get_all_tables(db: Session):
    """
    Получение всех записей из таблицы столов.
    """
    logger.info("Запрошен список всех столов.")
    return db.query(Table).all()


def create_table(db: Session, table: table_schema.TableCreate) -> Table:
    """
    Создание нового стола в базе данных.
    Если столик с таким именем уже существует, выбрасывается исключение.
    """
    # Проверяем, существует ли столик с таким же именем
    existing_table = db.query(Table).filter(Table.name == table.name).first()

    if existing_table:
        logger.warning("Столик с именем %s уже существует.", table.name)
        raise HTTPException(
            status_code=409,
            detail=f"Столик с именем '{table.name}' уже существует."
        )
    logger.info("Создание нового столика: %s", table.model_dump())
    db_table = Table(**table.model_dump())
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    logger.info("Столик создан с ID: %d", db_table.id)
    return db_table


def delete_table(db: Session, table_id: int) -> bool:
    """
    Удаление стола по его ID.
    """
    logger.info("Попытка удалить столик с ID: %d", table_id)
    table = db.get(Table, table_id)
    if table:
        db.delete(table)
        db.commit()
        logger.info("Столик с ID %d удалён.", table_id)
        return True
    logger.warning("Столик с ID %d не найден.", table_id)
    return False
