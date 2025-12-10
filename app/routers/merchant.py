from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.merchant import Merchant
from app.models.kyc import KYC
from app.schemas.merchant import MerchantCreate, KYCUpload

router = APIRouter(prefix='/merchant', tags=['merchant'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/create', status_code=201)
def create_merchant(payload: MerchantCreate, db: Session = Depends(get_db)):
    m = Merchant(user_id=payload.user_id, business_name=payload.business_name)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.post('/kyc/upload', status_code=201)
def upload_kyc(payload: KYCUpload, db: Session = Depends(get_db)):
    k = KYC(merchant_id=payload.merchant_id, pan_no=payload.pan_no, gst_no=payload.gst_no, bank_account=payload.bank_account)
    db.add(k)
    db.commit()
    db.refresh(k)
    return {'message': 'KYC uploaded', 'kyc_id': k.id}

@router.get('/status/{merchant_id}')
def merchant_status(merchant_id: int, db: Session = Depends(get_db)):
    m = db.query(Merchant).filter(Merchant.id==merchant_id).first()
    if not m:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Merchant not found')
    return {'merchant_id': m.id, 'status': m.status}

@router.get('/user/{user_id}')
def get_merchant_by_user(user_id: int, db: Session = Depends(get_db)):
    m = db.query(Merchant).filter(Merchant.user_id == user_id).first()
    if not m:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Merchant not found for this user')
    return m
