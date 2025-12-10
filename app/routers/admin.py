from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.merchant import Merchant
from app.models.transaction import Transaction

router = APIRouter(prefix='/admin', tags=['admin'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/merchants')
def all_merchants(db: Session = Depends(get_db)):
    return db.query(Merchant).all()

@router.post('/approve')
def approve_merchant(merchant_id: int, db: Session = Depends(get_db)):
    m = db.query(Merchant).filter(Merchant.id==merchant_id).first()
    if not m:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Merchant not found')
    m.status = 'verified'
    db.commit()
    return {'message': 'Merchant approved', 'merchant_id': m.id}

@router.get('/transactions')
def all_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()
