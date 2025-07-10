from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    limit = Column(Float, nullable=False)
    period = Column(String, nullable=False)  # e.g. "monthly", "weekly"

    user = relationship("User", back_populates="budgets")
