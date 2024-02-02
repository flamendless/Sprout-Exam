import os
import sqlite3

import pytest
from httpx import AsyncClient

from src.main import app

TEST_DB_NAME: str = "test.db"
if os.path.exists(TEST_DB_NAME):
    os.remove(TEST_DB_NAME)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    def fake_db():
        print("Using fake db")
        conn = sqlite3.connect(TEST_DB_NAME)
        return conn

    monkeypatch.setattr("src.db._get_db", fake_db)

    from src.db import setup_db
    setup_db()
