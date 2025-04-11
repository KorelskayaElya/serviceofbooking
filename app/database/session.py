"""Настройка подключения к базе данных и создание сессии SQLAlchemy."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение строки подключения из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL, future=True)

# Создание фабрики сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)