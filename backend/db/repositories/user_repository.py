from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self) -> User:
        new_user = User()
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user