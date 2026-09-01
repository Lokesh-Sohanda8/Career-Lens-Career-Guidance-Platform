"""Persistence operations for the identity domain."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domains.identity.models import Role, User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id).options(selectinload(User.roles)))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email).options(selectinload(User.roles)))
        return result.scalar_one_or_none()

    async def create(self, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def get_or_create_role(self, name: str) -> Role:
        result = await self.session.execute(select(Role).where(Role.name == name))
        role = result.scalar_one_or_none()
        if role:
            return role

        role = Role(name=name)
        self.session.add(role)
        await self.session.flush()
        return role

    async def assign_role(self, user: User, role: Role) -> None:
        if role not in user.roles:
            user.roles.append(role)
            await self.session.flush()
