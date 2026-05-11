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
                    quantity INTEGER NOT NULL,
                    item_id TEXT NOT NULL,
                    FOREIGN KEY (item_id) REFERENCES items(id)
                )
            """)
            )

            conn.execute(
                text(
                    "INSERT INTO orders (id, quantity, item_id) VALUES (:id, :quantity, :item_id)"
                ),
                [
                    {
                        "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                        "quantity": 5,
                        "item_id": "11111111-1111-1111-1111-111111111111",
                    },
                    {
                        "id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                        "quantity": 3,
                        "item_id": "22222222-2222-2222-2222-222222222222",
                    },
                    {
                        "id": "cccccccc-cccc-cccc-cccc-cccccccccccc",
                        "quantity": 7,
                        "item_id": "33333333-3333-3333-3333-333333333333",
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
