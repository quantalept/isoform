from fastapi import FastAPI
from app.api import user,product,purchase

app = FastAPI(title="FastAPI Template")

app.include_router(user.router, prefix="/api/v1", tags=["Users"])
app.include_router(product.router, prefix="/api/v1", tags=["Products"])
app.include_router(purchase.router, prefix="/api/v1", tags=["Purchases"])