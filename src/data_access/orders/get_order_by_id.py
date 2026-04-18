import sqlite3
from uuid import UUID

import src.data_access.errors as CommonDataAccessErrors
import src.data_access.orders.errors as DataAccessErrors
import src.data_access.orders.models as DataAccessModels


def get_order_by_id(db: sqlite3.Connection, id: UUID) -> DataAccessModels.GetOrderByID:
    """
    Fetches an order by ID from the database or raises an error.
    """
    try:
        cursor: sqlite3.Cursor = db.execute(
            "SELECT id, address, placed_on FROM orders WHERE id = ?",
            (str(id),),
        )
        row = cursor.fetchone()
    except sqlite3.Error as e:
        raise CommonDataAccessErrors.DatabaseError(str(e)) from e

    if row is None:
        raise DataAccessErrors.OrderNotFound(f"Failed to find order with id: {id}")

    return DataAccessModels.GetOrderByID.model_validate(dict(row))
