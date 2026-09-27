from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.engine import Connection

from fastapi_template.dependencies.get_db import get_db
from fastapi_template.dependencies.get_user import User, get_user
from fastapi_template.domains.orders.get_order_by_id.errors import DatabaseError

from .errors import OrderNotFoundError
from .get_order_by_id import get_order_by_id
from .models import OrderResponse

router = APIRouter()


@router.get("/{id}", response_model=OrderResponse)
async def handle_get_order_by_id(
    id: Annotated[UUID, Path(description="ID of the order")],
    db: Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """Retrieve an order by its ID."""

    try:
        return get_order_by_id(id=id, db=db)
    except OrderNotFoundError:
        raise HTTPException(status_code=404, detail="Order not found")
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Database error.")
