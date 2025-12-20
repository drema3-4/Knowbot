from backend.database.database import new_session, UserOrm, SessionOrm, QueryOrm, AnswerOrm
from main import SUserAdd, SUser, SSesionAdd, SQueryAdd, SAnswerAdd
from sqlalchemy import select

class UserRepository:
    @classmethod
    async def add_one(cls):
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
            user_schemas = [SUser.model_validate(user_model) for user_model in user_models]
            return user_schemas


class SessionRepository:
    @classmethod
    async def add_one(cls, data: SSesionAdd):
        async with new_session() as session:
            _session_dict = data.model_dump()
            _session = SessionOrm(**_session_dict)
            session.add(_session)
            await session.flush()
            await session.commit()

            return _session.session_id


class QueryRepository:
    @classmethod
    async def add_one(cls, data: SQueryAdd):
        async with new_session() as session:
            query_dict = data.model_dump()
            query = QueryOrm(**query_dict)
            session.add(query)
            await session.flush()
            await session.commit()

            return query.query_id

class AnswerRepository:
    @classmethod
    async def add_one(cls, data: SAnswerAdd):
        async with new_session() as session:
            answer_dict = data.model_dump()
            answer = AnswerOrm(**answer_dict)
            session.add(answer)
            await session.flush()
            await session.commit()

            return answer.answer_id