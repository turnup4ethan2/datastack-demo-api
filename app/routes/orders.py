from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from typing import Literal, Optional

router = APIRouter()


class OrderItem(BaseModel):
    product_id: str
    quantity: int
    unit_price_cents: int


class OrderCreate(BaseModel):
    user_id: str
    items: list[OrderItem]
    shipping_address: str
    promo_code: Optional[str] = None
    gift_message: Optional[str] = None   # NEW: attach a gift message to the order


class OrderStatusUpdate(BaseModel):
    status: Literal["pending", "confirmed", "shipped", "delivered", "cancelled"]
    tracking_number: Optional[str] = None


class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: list[OrderItem]
    shipping_address: str
    status: str
    total_cents: int
    promo_code: Optional[str]
    gift_message: Optional[str]
    tracking_number: Optional[str]
    created_at: str
    updated_at: str


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    body: OrderCreate,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """
    Place a new order. Inventory is reserved immediately; payment is captured
    asynchronously. Returns the order in 'pending' status.
    """
    total = sum(item.quantity * item.unit_price_cents for item in body.items)
    return {
        "id": "ord_001",
        "user_id": body.user_id,
        "items": [i.model_dump() for i in body.items],
        "shipping_address": body.shipping_address,
        "status": "pending",
        "total_cents": total,
        "promo_code": body.promo_code,
        "tracking_number": None,
        "created_at": "2026-03-20T00:00:00Z",
        "updated_at": "2026-03-20T00:00:00Z",
    }


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """Fetch a single order by ID. Users can only fetch their own orders."""
    return {
        "id": order_id,
        "user_id": "usr_abc123",
        "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}],
        "shipping_address": "123 Main St, San Francisco, CA 94105",
        "status": "shipped",
        "total_cents": 9998,
        "promo_code": None,
        "tracking_number": "1Z999AA10123456784",
        "created_at": "2026-03-18T10:00:00Z",
        "updated_at": "2026-03-19T08:30:00Z",
    }


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    body: OrderStatusUpdate,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """
    Update the status of an order. Only admins can transition to 'confirmed',
    'shipped', or 'delivered'. Users may cancel their own 'pending' orders.
    """
    return {
        "id": order_id,
        "user_id": "usr_abc123",
        "items": [{"product_id": "prod_001", "quantity": 2, "unit_price_cents": 4999}],
        "shipping_address": "123 Main St, San Francisco, CA 94105",
        "status": body.status,
        "total_cents": 9998,
        "promo_code": None,
        "tracking_number": body.tracking_number,
        "created_at": "2026-03-18T10:00:00Z",
        "updated_at": "2026-03-20T00:00:00Z",
    }
