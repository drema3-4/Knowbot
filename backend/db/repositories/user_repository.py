from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(
        self,
        user_name: str
    ) -> User:
        new_user = User(
            user_name=user_name
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    async def get_user_by_name(
        self,
        user_name: str
    ) -> User:
        stmt = select(User).where(
            User.user_name == user_name
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(
        self,
        user_id: int
    ) -> Optional[User]:
        stmt = select(User).where(
            User.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()