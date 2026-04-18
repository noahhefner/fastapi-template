import sqlite3
from uuid import UUID

import src.business_logic.errors as CommonBusinessLogicErrors
import src.business_logic.items.errors as BusinessLogicErrors
import src.business_logic.items.models as BusinessModels
import src.data_access.errors as CommonDataAccessErrors
import src.data_access.items as DataAccess
import src.data_access.items.errors as DataAccessErrors
import src.data_access.items.models as ItemDataAccessModels


def get_item_by_id(
    db: sqlite3.Connection,
    id: UUID,
) -> BusinessModels.GetItemByID:
    """
    Retrieves an item by ID, translating data access errors and returning a business model.
    """
    try:
        item: ItemDataAccessModels.GetItemByID = DataAccess.get_item_by_id(db, id)
    except CommonDataAccessErrors.DatabaseError as e:
        raise CommonBusinessLogicErrors.DatabaseError(str(e)) from e
    except DataAccessErrors.ItemNotFound as e:
        raise BusinessLogicErrors.ItemNotFound(str(e)) from e

    return BusinessModels.GetItemByID.model_validate(item)
