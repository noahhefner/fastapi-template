from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def get_db() -> Generator[Connection, None, None]:
    with engine.connect() as connection:
        yield connection
