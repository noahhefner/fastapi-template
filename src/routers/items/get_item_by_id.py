import sqlite3
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

import src.business_logic.errors as CommonBusinessErrors
import src.business_logic.items as BusinessLogic
import src.business_logic.items.errors as BusinessErrors
import src.business_logic.items.models as BusinessModels
import src.routers.items.response_models as ResponseModels
from src.db import get_db
from src.dependencies.get_user import get_user
from src.dependencies.get_user.models import User

router = APIRouter()


@router.get("/{id}", response_model=ResponseModels.GetItemByID)
def get_item_by_id(
    id: UUID,
    db: sqlite3.Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """
    Retrieves an item by ID and converts business logic errors into appropriate HTTP responses.
    """
    try:
        item: BusinessModels.GetItemByID = BusinessLogic.get_item_by_id(
            db,
            id,
        )
    except CommonBusinessErrors.DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )
    except BusinessErrors.ItemNotFound:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return item
