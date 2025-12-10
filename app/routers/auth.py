from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.database import SessionLocal
from app.models.user import User
from app.utils.jwt import create_access_token
from app.schemas.auth import RegisterIn, LoginIn, TokenOut

router = APIRouter(prefix='/auth', tags=['auth'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register', status_code=201)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email==payload.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered')
    hashed = bcrypt.hash(payload.password)
    user = User(name=payload.name, email=payload.email, password=hashed, role=payload.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'message': 'User registered', 'user_id': user.id}

@router.post('/login', response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==payload.email).first()
    if not user or not bcrypt.verify(payload.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token({'user_id': user.id, 'role': user.role})
    return {'access_token': token, 'role': user.role}
