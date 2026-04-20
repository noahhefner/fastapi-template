import sqlite3
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

import src.business_logic.errors as CommonBusinessErrors
import src.business_logic.orders as BusinessLogic
import src.business_logic.orders.errors as BusinessErrors
import src.business_logic.orders.models as BusinessModels
import src.routers.orders.response_models as ResponseModels
from src.dependencies.get_db import get_db

router = APIRouter()


@router.get("/{id}", response_model=ResponseModels.GetOrderByID)
def get_order_by_id(id: UUID, db: sqlite3.Connection = Depends(get_db)):
    """
    Retrieves an order by ID and converts domain errors into appropriate HTTP
    responses.
    """
    try:
        order: BusinessModels.GetOrderByID = BusinessLogic.get_order_by_id(
            db,
            id,
        )
    except CommonBusinessErrors.DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )
    except BusinessErrors.OrderNotFound:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order
