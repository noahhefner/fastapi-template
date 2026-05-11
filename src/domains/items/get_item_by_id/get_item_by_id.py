from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection

from src.dependencies.get_db import get_db
from src.dependencies.get_user import User, get_user

router = APIRouter()


class ItemResponse(BaseModel):
    id: UUID
    name: str
    quantity: int


@router.get("/{id}", response_model=ItemResponse)
async def get_item_by_id(
    id: Annotated[UUID, Path(description="ID of the item")],
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve an item by its ID."""

    query = text("SELECT id, name, quantity FROM items WHERE id = :id")

    params = {"id": str(id)}

    try:
        result = db.execute(query, params)
        row = result.mappings().one_or_none()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    return row
