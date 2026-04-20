import sqlite3

from fastapi import APIRouter, Depends, HTTPException

import src.business_logic.errors as CommonBusinessErrors
import src.business_logic.items as BusinessLogic
import src.business_logic.items.models as BusinessModels
import src.routers.items.response_models as ResponseModels
from src.dependencies.get_db import get_db
from src.dependencies.get_user import (get_user, User)

router = APIRouter()


@router.get("/", response_model=list[ResponseModels.GetAllItems])
def get_all_items(
    db: sqlite3.Connection = Depends(get_db),
    user: User = Depends(get_user),
):
    """
    Retrieves all items and converts business logic errors into appropriate HTTP responses.
    """

    try:
        items: list[BusinessModels.GetAllItems] = BusinessLogic.get_all_items(db)
    except CommonBusinessErrors.DatabaseError:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )

    return items
