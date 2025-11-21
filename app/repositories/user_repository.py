from datetime import datetime
from uuid import UUID
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.entities.user import User
from app.infrastructure.security import get_password_hash


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, login: str, password: str, project_id: UUID, env: str, domain: str) -> User:
        hashed_password = get_password_hash(password)
        user = User(
            login=login,
            password=hashed_password,
            project_id=project_id,
            env=env,
            domain=domain,
        )
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError as e:
            await self.session.rollback()
            error_str = str(e.orig).lower() if hasattr(e, 'orig') else str(e).lower()
            if "unique" in error_str or "duplicate" in error_str or "already exists" in error_str or "violates unique constraint" in error_str:
                raise ValueError(f"user with login {login} already exists") from e
            raise ValueError(f"database integrity error: {str(e)}") from e
        except Exception as e:
            await self.session.rollback()
            raise ValueError(f"failed to create user: {str(e)}") from e

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_login(self, login: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.login == login))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    async def update_locktime(self, user_id: UUID, locktime: Optional[datetime]) -> Optional[User]:
        await self.session.execute(
            update(User).where(User.id == user_id).values(locktime=locktime)
        )
        await self.session.commit()
        return await self.get_by_id(user_id)

