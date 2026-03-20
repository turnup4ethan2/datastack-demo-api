from fastapi import APIRouter, Header, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class ProductCreate(BaseModel):
    name: str
    description: str
    price_cents: int           # price in cents (USD)
    sku: str
    inventory_count: int = 0
    tags: list[str] = []


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price_cents: int
    sku: str
    inventory_count: int
    tags: list[str]
    created_at: str


@router.get("", response_model=list[ProductResponse])
def list_products(
    tag: Optional[str] = None,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """List all products. Optionally filter by tag."""
    return []


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    body: ProductCreate,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """Create a new product in the catalog."""
    return {
        "id": "prod_001",
        "name": body.name,
        "description": body.description,
        "price_cents": body.price_cents,
        "sku": body.sku,
        "inventory_count": body.inventory_count,
        "tags": body.tags,
        "created_at": "2026-03-20T00:00:00Z",
    }


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """Fetch a single product by ID."""
    return {
        "id": product_id,
        "name": "Widget Pro",
        "description": "Our best-selling widget.",
        "price_cents": 4999,
        "sku": "WGT-PRO-001",
        "inventory_count": 142,
        "tags": ["hardware", "featured"],
        "created_at": "2026-01-15T00:00:00Z",
    }
