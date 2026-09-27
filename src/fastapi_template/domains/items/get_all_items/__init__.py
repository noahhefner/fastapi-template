import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

from fastapi_template.dependencies.get_db import get_db
from fastapi_template.dependencies.get_user import User, get_user

logger = logging.getLogger(__name__)

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
    except SQLAlchemyError as e:
        logger.error(f"Exception while getting all items: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return rows
