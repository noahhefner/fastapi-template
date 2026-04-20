import sqlite3

import src.business_logic.errors as CommonBusinessLogicErrors
import src.business_logic.items.models as BusinessModels
import src.data_access.errors as CommonDataAccessErrors
import src.data_access.items as DataAccess
import src.data_access.items.models as ItemDataAccessModels


def get_all_items(db: sqlite3.Connection) -> list[BusinessModels.GetAllItems]:
    """
    Retrieves all items translating data access errors and returning a business model.
    """
    try:
        items: list[ItemDataAccessModels.GetAllItems] = DataAccess.get_all_items(db)
    except CommonDataAccessErrors.DatabaseError as e:
        raise CommonBusinessLogicErrors.DatabaseError(str(e)) from e

    return [BusinessModels.GetAllItems.model_validate(item) for item in items]
