import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

router = APIRouter(prefix='/transaction', tags=['transaction'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    ref = str(uuid.uuid4())[:12]
    tx = Transaction(
        merchant_id=payload.merchant_id, 
        amount=payload.amount, 
        reference_id=ref,
        items=payload.items,
        address=payload.address
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return {'message': 'Transaction created', 'reference_id': tx.reference_id, 'tx_id': tx.id}

@router.post('/update-status')
def update_status(payload: TransactionUpdate, db: Session = Depends(get_db)):
    tx = db.query(Transaction).filter(Transaction.id==payload.tx_id).first()
    if not tx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Transaction not found')
    tx.status = payload.status
    db.commit()
    return {'message': 'Transaction updated', 'tx_id': tx.id, 'status': tx.status}

from datetime import datetime, timedelta
from sqlalchemy import func

@router.get('/history/{merchant_id}')
def list_transactions(merchant_id: int, db: Session = Depends(get_db)):
    rows = db.query(Transaction).filter(Transaction.merchant_id==merchant_id).order_by(Transaction.created_at.desc()).all()
    return rows

@router.get('/analytics/{merchant_id}')
def get_analytics(merchant_id: int, db: Session = Depends(get_db)):
    # Calculate last 7 days sales
    today = datetime.now()
    seven_days_ago = today - timedelta(days=6)
    
    # Query transactions from last 7 days that are successful
    txs = db.query(Transaction).filter(
        Transaction.merchant_id == merchant_id,
        Transaction.status == 'success',
        Transaction.created_at >= seven_days_ago
    ).all()
    
    # Initialize 7 day map
    data_map = {}
    for i in range(7):
        day_str = (seven_days_ago + timedelta(days=i)).strftime('%Y-%m-%d')
        data_map[day_str] = 0.0
        
    total_sales = 0.0
    for tx in txs:
        # Check if created_at is datetime object, if so convert to string
        if isinstance(tx.created_at, datetime):
            day_str = tx.created_at.strftime('%Y-%m-%d')
        else:
            day_str = str(tx.created_at)[:10]
            
        if day_str in data_map:
            data_map[day_str] += tx.amount
            total_sales += tx.amount
            
    # Prepare result for Chart Kit
    labels = []
    values = []
    headers = sorted(data_map.keys())
    for day in headers:
        labels.append(day[5:]) # MM-DD
        values.append(data_map[day])
        
    return {
        "labels": labels,
        "data": values,
        "total_sales": total_sales,
        "success_rate": 100 if txs else 0 # Simplified
    }
