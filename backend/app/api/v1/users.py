"""Authenticated user endpoints."""

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.domains.identity.schemas import UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def me(user=Depends(get_current_user)):
    return UserRead(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        roles=[role.name for role in user.roles],
        created_at=user.created_at,
    )
