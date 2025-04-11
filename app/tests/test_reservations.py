"""Тесты для эндпоинта резерва столиков."""

import uuid
import pytest


@pytest.mark.asyncio
async def test_create_reservation(client):
    """
    Проверяет успешное создание новой брони.
    """
    table_name = f"Table {uuid.uuid4()}"
    table_data = {
        "name": table_name,
        "seats": 4,
        "location": "Test Area"
    }

    table_resp = await client.post("/tables/", json=table_data)
    assert table_resp.status_code == 200
    table_id = table_resp.json()["id"]

    reservation_data = {
        "customer_name": "Костя Петров",
        "table_id": table_id,
        "reservation_time": "2025-04-09T15:00:00",
        "duration_minutes": 60
    }

    response = await client.post("/reservations/", json=reservation_data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["customer_name"] == "Костя Петров"
    assert data["table_id"] == table_id
    assert data["duration_minutes"] == 60


@pytest.mark.asyncio
async def test_reservation_conflict(client):
    """
    Проверяет, что нельзя создать две брони на один и тот же столик в одно и то же время.
    """
    table_name = f"ConflictTable {uuid.uuid4()}"
    table_resp = await client.post("/tables/", json={
        "name": table_name,
        "seats": 2,
        "location": "Test zone"
    })
    assert table_resp.status_code == 200
    table_id = table_resp.json()["id"]

    # Первая бронь
    await client.post("/reservations/", json={
        "customer_name": "Пётр",
        "table_id": table_id,
        "reservation_time": "2025-04-09T18:00:00",
        "duration_minutes": 60
    })

    # Вторая бронь с пересечением
    conflict_resp = await client.post("/reservations/", json={
        "customer_name": "Мария",
        "table_id": table_id,
        "reservation_time": "2025-04-09T18:30:00",
        "duration_minutes": 30
    })

    assert conflict_resp.status_code == 409
    assert "уже забронирован" in conflict_resp.text.lower()
