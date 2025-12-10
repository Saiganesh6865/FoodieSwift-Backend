from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, merchant, transaction, admin, razorpay_integration, products

Base.metadata.create_all(bind=engine)

app = FastAPI(title='MiniPay – Payment Gateway Simulation with Razorpay')

app.include_router(auth.router)
app.include_router(merchant.router)
app.include_router(transaction.router)
app.include_router(admin.router)
app.include_router(razorpay_integration.router)
app.include_router(products.router)

@app.get('/health')
def health():
    return {'status': 'ok'}
