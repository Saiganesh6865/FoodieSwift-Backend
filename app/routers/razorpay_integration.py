import razorpay
from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from app.models.transaction import Transaction
import uuid

router = APIRouter(prefix="/razorpay", tags=["razorpay"])

client = razorpay.Client(auth=(RAZORPAY_KEY_ID or "", RAZORPAY_KEY_SECRET or ""))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel

class OrderCreate(BaseModel):
    amount: float
    merchant_id: int
    mock_mode: bool = False
    items: str | None = None
    address: str | None = None

@router.post('/create-order', status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    try:
        amount = payload.amount
        merchant_id = payload.merchant_id
        
        if payload.mock_mode:
            # Mock Mode: Simulate success immediately
            fake_order_id = f"order_mock_{uuid.uuid4().hex[:10]}"
            fake_tx_id = f"pay_mock_{uuid.uuid4().hex[:10]}"
            
            tx = Transaction(
                merchant_id=merchant_id, 
                amount=amount, 
                status="created", 
                reference_id=fake_order_id,
                items=payload.items,
                address=payload.address
            )
            db.add(tx)
            db.commit()
            db.refresh(tx)
            
            return {
                "message": "Mock Order created", 
                "order_id": fake_order_id, 
                "amount": amount, 
                "currency": "INR", 
                "tx_id": tx.id,
                "is_mock": True
            }

        razorpay_amount = int(amount * 100)
        order = client.order.create({"amount": razorpay_amount, "currency": "INR", "receipt": str(uuid.uuid4())})

        tx = Transaction(
            merchant_id=merchant_id, 
            amount=amount, 
            status="created", 
            reference_id=order.get('id'),
            items=payload.items,
            address=payload.address
        )
        db.add(tx)
        db.commit()
        db.refresh(tx)

        return {"message": "Order created", "order_id": order.get('id'), "amount": amount, "currency": "INR", "tx_id": tx.id}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post('/webhook')
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.json()
    order_id = payload.get('payload', {}).get('payment', {}).get('entity', {}).get('order_id')
    status = payload.get('event')

    if not order_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid webhook payload')

    tx = db.query(Transaction).filter(Transaction.reference_id == order_id).first()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Transaction not found')

    if status == 'payment.captured':
        tx.status = 'success'
    elif status == 'payment.failed':
        tx.status = 'failed'
    else:
        tx.status = status.replace('payment.', '')

    db.commit()
    return {'message': 'Webhook processed', 'tx_id': tx.id, 'status': tx.status}
