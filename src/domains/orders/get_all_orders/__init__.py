from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user

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
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

    return rows
