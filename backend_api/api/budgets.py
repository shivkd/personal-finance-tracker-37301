from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.database import get_db
from core.auth import get_current_user
from schemas.budget import BudgetCreate, BudgetRead, BudgetUpdate, BudgetProgress
from models.budget import Budget
from models.user import User

router = APIRouter()

# PUBLIC_INTERFACE
@router.get("/", response_model=List[BudgetRead], summary="List all budgets")
async def list_budgets(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(Budget).where(Budget.user_id == user.id))
    return results.scalars().all()

# PUBLIC_INTERFACE
@router.post("/", response_model=BudgetRead, summary="Create budget")
async def create_budget(budget: BudgetCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    b = Budget(**budget.dict(), user_id=user.id)
    db.add(b)
    await db.commit()
    await db.refresh(b)
    return b

# PUBLIC_INTERFACE
@router.put("/{budget_id}", response_model=BudgetRead, summary="Update a budget")
async def update_budget(budget_id: int, update: BudgetUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Budget).where(Budget.id == budget_id, Budget.user_id == user.id))
    b = result.scalar()
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(b, key, value)
    await db.commit()
    await db.refresh(b)
    return b

# PUBLIC_INTERFACE
@router.delete("/{budget_id}", summary="Delete budget")
async def delete_budget(budget_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Budget).where(Budget.id == budget_id, Budget.user_id == user.id))
    b = result.scalar()
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(b)
    await db.commit()
    return {"ok": True}

# PUBLIC_INTERFACE
@router.get("/progress/{budget_id}", response_model=BudgetProgress, summary="Get budget progress")
async def budget_progress(budget_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Placeholder: Should aggregate associated transactions to measure budget use
    result = await db.execute(select(Budget).where(Budget.id == budget_id, Budget.user_id == user.id))
    b = result.scalar()
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    # Return dummy value
    return BudgetProgress(budget_id=b.id, total_spent=0, limit=b.limit, percent=0.0, alert=False)
