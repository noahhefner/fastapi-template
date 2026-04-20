import sqlite3
from typing import Generator

DATABASE_PATH = "database.db"


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    FastAPI dependency that provides a SQLite connection.
    Intended for local testing.
    """
    conn = sqlite3.connect(DATABASE_PATH)

    # Return rows as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()
