from app.database import SessionLocal
from app.models.user import User
from app.models.merchant import Merchant

db = SessionLocal()
users = db.query(User).all()
print(f"Total Users: {len(users)}")
for u in users:
    print(f"ID: {u.id}, Email: {u.email}, Role: {u.role}")
    merchant = db.query(Merchant).filter(Merchant.user_id == u.id).first()
    if merchant:
        print(f"  -> Merchant ID: {merchant.id}, Business: {merchant.business_name}")
    else:
        print(f"  -> No Merchant Profile")

db.close()
