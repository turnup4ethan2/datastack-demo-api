from fastapi import FastAPI
from app.routes import users, products, orders

app = FastAPI(
    title="DataStack API",
    version="2.1.0",
    description="DataStack core API — user management, product catalog, and order processing.",
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/health")
def health():
    return {"status": "ok"}
