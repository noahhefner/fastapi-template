from fastapi import APIRouter

from . import get_all_items

router = APIRouter()

router.include_router(get_all_items.router)
