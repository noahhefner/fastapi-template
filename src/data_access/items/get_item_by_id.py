import sqlite3
from uuid import UUID

import src.data_access.errors as CommonDataAccessErrors
import src.data_access.items.errors as DataAccessErrors
import src.data_access.items.models as DataAccessModels


def get_item_by_id(db: sqlite3.Connection, id: UUID) -> DataAccessModels.GetItemByID:
    """
    Fetches an item by ID from the database or raises an error.
    """
    try:
        cursor: sqlite3.Cursor = db.execute(
            "SELECT id, name, quantity FROM items WHERE id = ?",
            (str(id),),
        )
        row = cursor.fetchone()
    except sqlite3.Error as e:
        raise CommonDataAccessErrors.DatabaseError(str(e)) from e

    if row is None:
        raise DataAccessErrors.ItemNotFound(f"Failed to find item with id: {id}")

    return DataAccessModels.GetItemByID.model_validate(dict(row))
