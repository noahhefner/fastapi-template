from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user

router = APIRouter()


class AllItemsResponse(BaseModel):
    id: UUID
    name: str
    quantity: int


@router.get("/{id}", response_model=list[AllItemsResponse])
async def get_item_by_id(
    id: Annotated[UUID, Path(description="ID of the item")],
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve an item by its ID."""

    query = text("SELECT id, name, quantity FROM items WHERE ID = %()s")

    try:
        result = db.execute(query)
        rows = result.mappings().all()
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

    return rows
