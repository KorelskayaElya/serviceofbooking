"""Тесты для эндпоинта создания столика."""

import uuid
import pytest


@pytest.mark.asyncio
async def test_create_table(client):
    """
    Проверяет успешное создание нового столика через POST-запрос.
    """
    name = f"Test Table {uuid.uuid4()}"
    response = await client.post("/tables/", json={
        "name": name,
        "seats": 4,
        "location": "Тестовая зона"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == name
    assert data["seats"] == 4
    assert data["location"] == "Тестовая зона"


@pytest.mark.asyncio
async def test_create_existing_table(client):
    """
    Проверяет создание столика с уже существующим именем.
    """
    name = f"Test Table {uuid.uuid4()}"
    # Создаём первый столик
    await client.post("/tables/", json={
        "name": name,
        "seats": 4,
        "location": "Test Zone"
    })
    # Пытаемся создать столик с тем же именем
    response = await client.post("/tables/", json={
        "name": name,
        "seats": 4,
        "location": "Test Zone"
    })

    assert response.status_code == 409
    assert "Столик с именем" in response.text


@pytest.mark.asyncio
async def test_delete_existing_table(client):
    """
    Проверяет удаление существующего столика.
    """
    name = f"Test Table {uuid.uuid4()}"
    create_resp = await client.post("/tables/", json={
        "name": name,
        "seats": 4,
        "location": "Тестовая зона"
    })
    table_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/tables/{table_id}")
    assert delete_resp.status_code == 204


@pytest.mark.asyncio
async def test_delete_nonexistent_table(client):
    """
    Проверяет удаление несуществующего столика (ожидается 404).
    """
    delete_resp = await client.delete("/tables/99999")
    assert delete_resp.status_code == 404
    assert "table not found" in delete_resp.text.lower()