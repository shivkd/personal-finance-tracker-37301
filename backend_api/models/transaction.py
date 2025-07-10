from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    category = Column(String)
    tags = Column(ARRAY(String), default=[])

    user = relationship("User", back_populates="transactions")
