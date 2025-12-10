from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Merchant(Base):
    __tablename__ = "merchants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    business_name = Column(String, nullable=False)
    status = Column(String, default="pending", nullable=False)
