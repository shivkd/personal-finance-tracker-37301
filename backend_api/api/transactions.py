from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from core.database import get_db
from core.auth import get_current_user
from schemas.transaction import TransactionRead, TransactionCreate, TransactionUpdate
from models.transaction import Transaction
from models.user import User

router = APIRouter()

# PUBLIC_INTERFACE
@router.get("/", response_model=List[TransactionRead], summary="Get transactions with filter")
async def list_transactions(
    user: User = Depends(get_current_user),
    category: Optional[str] = None,
    tag: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Transaction).where(Transaction.user_id == user.id)
    if category:
        stmt = stmt.where(Transaction.category == category)
    if tag:
        stmt = stmt.where(Transaction.tags.any(tag))
    results = await db.execute(stmt)
    return results.scalars().all()

# PUBLIC_INTERFACE
@router.post("/", response_model=TransactionRead, summary="Create new transaction")
async def create_transaction(
    txn: TransactionCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    t = Transaction(**txn.dict(), user_id=user.id)
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return t

# PUBLIC_INTERFACE
@router.put("/{transaction_id}", response_model=TransactionRead, summary="Update a transaction")
async def update_transaction(
    transaction_id: int, update: TransactionUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id).where(Transaction.user_id == user.id))
    transaction = result.scalar()
    if not transaction:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(transaction, key, value)
    await db.commit()
    await db.refresh(transaction)
    return transaction

# PUBLIC_INTERFACE
@router.delete("/{transaction_id}", summary="Delete a transaction")
async def delete_transaction(transaction_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id).where(Transaction.user_id == user.id))
    transaction = result.scalar()
    if not transaction:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(transaction)
    await db.commit()
    return {"ok": True}
