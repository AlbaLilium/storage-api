from fastapi import FastAPI

from app.api.v1.order_router import order_router
from app.api.v1.product_router import product_router

app = FastAPI()
app.include_router(product_router)
app.include_router(order_router)