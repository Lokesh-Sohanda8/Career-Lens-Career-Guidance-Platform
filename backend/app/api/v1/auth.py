"""Authentication endpoints."""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.domains.identity.schemas import Token, UserCreate, UserRead
from app.domains.identity.service import IdentityService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _to_read(user) -> UserRead:
    return UserRead(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        roles=[role.name for role in user.roles],
        created_at=user.created_at,
    )


@router.post("/register", response_model=UserRead, status_code=201)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await IdentityService(db).register(payload.email, payload.password)
    return _to_read(user)


@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await IdentityService(db).authenticate(form.username, form.password)
    return Token(access_token=IdentityService(db).issue_token(user))
