import sqlite3

import src.data_access.errors as CommonDataAccessErrors
import src.data_access.items.models as DataAccessModels


def get_all_items(db: sqlite3.Connection) -> list[DataAccessModels.GetAllItems]:
    """
    Fetches all items from the database or raises an error.
    """
    try:
        cursor: sqlite3.Cursor = db.execute("SELECT id, name, quantity FROM items", ())
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        raise CommonDataAccessErrors.DatabaseError(str(e)) from e

    return [DataAccessModels.GetAllItems.model_validate(dict(row)) for row in rows]
