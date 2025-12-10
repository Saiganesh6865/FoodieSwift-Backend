from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class KYC(Base):
    __tablename__ = "kyc"
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    pan_no = Column(String)
    gst_no = Column(String)
    bank_account = Column(String)
    status = Column(String, default="pending")
