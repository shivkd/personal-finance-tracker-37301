from typing import Optional
from pydantic import BaseModel

# PUBLIC_INTERFACE
class BudgetBase(BaseModel):
    name: str
    limit: float
    period: str  # e.g. "monthly", "yearly"

# PUBLIC_INTERFACE
class BudgetCreate(BudgetBase):
    pass

# PUBLIC_INTERFACE
class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    limit: Optional[float] = None
    period: Optional[str] = None

# PUBLIC_INTERFACE
class BudgetRead(BudgetBase):
    id: int

    class Config:
        orm_mode = True

# PUBLIC_INTERFACE
class BudgetProgress(BaseModel):
    budget_id: int
    total_spent: float
    limit: float
    percent: float
    alert: bool
