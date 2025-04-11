"""Главный файл запуска FastAPI-приложения для бронирования столиков."""

import logging
from fastapi import FastAPI
from app.routers import reservation_router, table_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Создаём приложение FastAPI
app = FastAPI(
    title="Restaurant Booking API",
    description="API-сервис для бронирования столиков в ресторане",
    version="1.0.0",
)

# Подключаем роутеры
app.include_router(
    reservation_router.router,
    prefix="/reservations",
    tags=["Reservations"],
)
app.include_router(
    table_router.router,
    prefix="/tables",
    tags=["Tables"],
)

# Тестовый корневой эндпоинт
@app.get("/")
def root() -> dict[str, str]:
    """
    Корневой эндпоинт
    """
    return {"message": "Добро пожаловать в сервис бронирования столиков!"}
