from pydantic import BaseModel

class TransactionCreate(BaseModel):
    merchant_id: int
    amount: float
    items: str | None = None
    address: str | None = None

class TransactionUpdate(BaseModel):
    tx_id: int
    status: str
