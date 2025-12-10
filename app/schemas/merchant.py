from pydantic import BaseModel

class MerchantCreate(BaseModel):
    user_id: int
    business_name: str

class KYCUpload(BaseModel):
    merchant_id: int
    pan_no: str
    gst_no: str
    bank_account: str
