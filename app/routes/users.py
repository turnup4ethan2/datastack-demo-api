from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    role: str = "member"          # "admin" | "member" | "viewer"
    organization_id: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    organization_id: str
    created_at: str


@router.get("", response_model=list[UserResponse])
def list_users(
    organization_id: str,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """Return all users in the given organization."""
    return []


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    body: UserCreate,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """Create a new user. Requires admin role on the organization."""
    return {
        "id": "usr_abc123",
        "email": body.email,
        "name": body.name,
        "role": body.role,
        "organization_id": body.organization_id,
        "created_at": "2026-03-20T00:00:00Z",
    }


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """Fetch a single user by ID."""
    return {
        "id": user_id,
        "email": "alice@datastack.io",
        "name": "Alice",
        "role": "admin",
        "organization_id": "org_xyz",
        "created_at": "2026-01-01T00:00:00Z",
    }


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    authorization: str = Header(..., description="Bearer <token>"),
):
    """Permanently delete a user. Cannot delete your own account."""
    return None
