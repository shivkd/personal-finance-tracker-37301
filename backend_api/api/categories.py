from fastapi import APIRouter
from typing import List

router = APIRouter()

# PUBLIC_INTERFACE
@router.get("/", response_model=List[str], summary="List available categories")
async def list_categories():
    return ["Groceries", "Dining", "Salary", "Travel", "Shopping", "Bills", "Other"]
