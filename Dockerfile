# Используем официальный базовый образ Python
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip --no-cache-dir && \
    pip install --no-cache-dir -r requirements.txt

# Копируем всё остальное приложение
COPY . .

# Команда запуска приложения
CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000", "--reload"]
