import logging
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

from fastapi_template.domains.orders.get_order_by_id.errors import DatabaseError

from .errors import OrderNotFoundError

logger = logging.getLogger(__name__)


def get_order_by_id(id: UUID, db: Connection):
    """Fetch an order from the database by its ID.

    Raises OrderNotFoundError if no matching order exists.
    """

    query = text("SELECT id, quantity, item_id FROM orders WHERE id = :id")
    params = {"id": str(id)}

    try:
        result = db.execute(query, params)
        row = result.mappings().one_or_none()
    except SQLAlchemyError as e:
        logger.erorr(f"Database error while getting order by ID: {e}")
        raise DatabaseError(str(e))

    if not row:
        raise OrderNotFoundError(id)

    return row
