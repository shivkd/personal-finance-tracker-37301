from typing import Optional, List
from pydantic import BaseModel
from datetime import date

# PUBLIC_INTERFACE
class TransactionBase(BaseModel):
    amount: float
    date: date
    description: Optional[str] = ""
    category: Optional[str] = None
    tags: List[str] = []

# PUBLIC_INTERFACE
class TransactionCreate(TransactionBase):
    pass

# PUBLIC_INTERFACE
class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    date: Optional[date] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

# PUBLIC_INTERFACE
class TransactionRead(TransactionBase):
    id: int

    class Config:
        orm_mode = True
