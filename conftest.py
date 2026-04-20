import sqlite3
import tempfile

import pytest
from fastapi.testclient import TestClient

from src.dependencies.get_db import get_db
from src.main import app


@pytest.fixture
def client():
    with tempfile.NamedTemporaryFile() as tmp:

        def override_get_db():
            conn = sqlite3.connect(tmp.name)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()

        conn = sqlite3.connect(tmp.name)
        cursor = conn.cursor()

        # ---- ITEMS TABLE ----
        cursor.execute("""
            CREATE TABLE items (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)

        item_test_data = [
            ("11111111-1111-1111-1111-111111111111", "Apples", 10),
            ("22222222-2222-2222-2222-222222222222", "Bananas", 25),
            ("33333333-3333-3333-3333-333333333333", "Oranges", 15),
        ]

        cursor.executemany(
            "INSERT INTO items (id, name, quantity) VALUES (?, ?, ?)", item_test_data
        )

        # ---- ORDERS TABLE ----
        cursor.execute("""
            CREATE TABLE orders (
                id TEXT PRIMARY KEY,
                address TEXT NOT NULL,
                placed_on TEXT NOT NULL
            )
        """)

        order_test_data = [
            (
                "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "123 Main St, Springfield, USA",
                "2024-01-01T10:00:00",
            ),
            (
                "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
                "456 Elm St, Metropolis, USA",
                "2024-02-15T14:30:00",
            ),
            (
                "cccccccc-cccc-cccc-cccc-cccccccccccc",
                "789 Oak Ave, Gotham, USA",
                "2024-03-10T09:15:00",
            ),
        ]

        cursor.executemany(
            "INSERT INTO orders (id, address, placed_on) VALUES (?, ?, ?)",
            order_test_data,
        )

        conn.commit()
        conn.close()

        app.dependency_overrides[get_db] = override_get_db

        with TestClient(app) as client:
            yield client

        app.dependency_overrides.clear()
