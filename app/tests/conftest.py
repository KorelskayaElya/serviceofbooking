"""Фикстуры"""

from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.fixture(name="transport")
def fixture_transport() -> ASGITransport:
    """
    Возвращает транспорт для асинхронного клиента HTTPX с FastAPI-приложением.
    """
    return ASGITransport(app=app)


@pytest_asyncio.fixture(name="client")
async def fixture_client(transport: ASGITransport) -> AsyncGenerator[AsyncClient, None]:
    """
    Возвращает асинхронный клиент HTTPX с использованием переданного транспорта.
    """
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
