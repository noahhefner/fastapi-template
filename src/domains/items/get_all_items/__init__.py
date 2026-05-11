from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user

router = APIRouter()


class AllItemsResponse(BaseModel):
    """Response model for the list of all items."""

    id: UUID
    name: str
    quantity: int


@router.get("/", response_model=list[AllItemsResponse])
async def get_all_items(
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve all items."""

    query = text("SELECT id, name, quantity FROM items")

    try:
        result = db.execute(query)
        rows = result.mappings().all()
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

    return rows
