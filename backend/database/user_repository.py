from sqlalchemy import select
from database.database import new_session, UserOrm
from models.user_schemas import SUser


class UserRepository:
    @classmethod
    async def add_one(cls) -> int:
        async with new_session() as session:
            user = UserOrm()
            session.add(user)
            await session.flush()
            await session.commit()

            return user.user_id
        
    @classmethod
    async def find_all(cls) -> list[SUser]:
        async with new_session() as session:
            request = select(UserOrm)
            result = await session.execute(request)
            user_models = result.scalars().all()
            # user_schemas = [SUser.model_validate(user_model) for user_model in user_models]
            return user_models