import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

from fastapi_template.dependencies.get_db import get_db
from fastapi_template.dependencies.get_user import User, get_user

logger: logging.Logger = logging.getLogger(__name__)
router = APIRouter()


class AllOrdersResponse(BaseModel):
    """Response model for the list of all orders."""

    id: UUID
    quantity: int
    item_id: UUID


@router.get("/", response_model=list[AllOrdersResponse])
async def get_all_orders(
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve all orders."""

    query = text("SELECT id, quantity, item_id FROM orders")

    try:
        result = db.execute(query)
        rows = result.mappings().all()
    except SQLAlchemyError:
        logger.error("Database error while getting all orders: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return rows
