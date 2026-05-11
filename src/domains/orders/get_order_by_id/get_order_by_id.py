from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection

from .errors import OrderNotFoundError


def get_order_by_id(id: UUID, db: Connection):
    """Fetch an order from the database by its ID.

    Raises OrderNotFoundError if no matching order exists.
    """

    query = text("SELECT id, quantity, item_id FROM orders WHERE id = :id")
    params = {"id": str(id)}

    try:
        result = db.execute(query, params)
        row = result.mappings().one_or_none()
    except Exception:
        raise

    if not row:
        raise OrderNotFoundError(id)

    return row
