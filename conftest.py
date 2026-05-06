import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from src.dependencies.get_db import get_db
from src.main import app


@pytest.fixture
def client():
    with tempfile.NamedTemporaryFile() as tmp:
        DATABASE_URL = f"sqlite:///{tmp.name}"

        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
        )

        # ---- Create schema + seed data ----
        with engine.connect() as conn:
            # ITEMS TABLE
            conn.execute(
                text("""
                CREATE TABLE items (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL
                )
            """)
            )

            conn.execute(
                text("INSERT INTO items (id, name, quantity) VALUES (:id, :name, :quantity)"),
                [
                    {
                        "id": "11111111-1111-1111-1111-111111111111",
                        "name": "Apples",
                        "quantity": 10,
                    },
                    {
                        "id": "22222222-2222-2222-2222-222222222222",
                        "name": "Bananas",
                        "quantity": 25,
                    },
                    {
                        "id": "33333333-3333-3333-3333-333333333333",
                        "name": "Oranges",
                        "quantity": 15,
                    },
                ],
            )

            # ORDERS TABLE
            conn.execute(
                text("""
                CREATE TABLE orders (
                    id TEXT PRIMARY KEY,
                    address TEXT NOT NULL,
                    placed_on TEXT NOT NULL
                )
            """)
            )

            conn.execute(
                text(
                    "INSERT INTO orders (id, address, placed_on) VALUES (:id, :address, :placed_on)"
                ),
                [
                    {
                        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "address": "123 Main St, Springfield, USA",
                        "placed_on": "2024-01-01T10:00:00",
                    },
                    {
                        "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                        "address": "456 Elm St, Metropolis, USA",
                        "placed_on": "2024-02-15T14:30:00",
                    },
                    {
                        "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
                        "address": "789 Oak Ave, Gotham, USA",
                        "placed_on": "2024-03-10T09:15:00",
                    },
                ],
            )

            conn.commit()

        # ---- Override dependency ----
        def override_get_db():
            with engine.connect() as connection:
                yield connection

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app) as client:
            yield client

        app.dependency_overrides.clear()
