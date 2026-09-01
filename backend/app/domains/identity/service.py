"""Identity business logic."""

import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.domains.identity.models import User
from app.domains.identity.repository import UserRepository


class IdentityService:
    DEFAULT_STUDENT_ROLE = "student"

    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def register(self, email: str, password: str) -> User:
        normalized_email = email.strip().lower()

        if await self.users.get_by_email(normalized_email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            )

        user = await self.users.create(
            email=normalized_email,
            password_hash=hash_password(password),
        )
        role = await self.users.get_or_create_role(self.DEFAULT_STUDENT_ROLE)
        await self.users.assign_role(user, role)

        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists.",
            ) from None

        await self.session.refresh(user)
        return user

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.users.get_by_email(email.strip().lower())

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive.",
            )

        return user

    def issue_token(self, user: User) -> str:
        return create_access_token({"sub": str(user.id)})

    async def get_current_user(self, user_id: uuid.UUID) -> User:
        user = await self.users.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
