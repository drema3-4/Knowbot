from sqlalchemy import select
from database.database import new_session, SessionOrm
from models.session_schemas import SSession, SSessionAdd

class SessionRepository:
    @classmethod
    async def add_one(cls, data: SSessionAdd):
        async with new_session() as session:
            _session_dict = data.model_dump()
            _session = SessionOrm(**_session_dict)
            session.add(_session)
            await session.flush()
            await session.commit()

            return _session.session_id
        
    @classmethod
    async def find_all(cls) -> list[SSession]:
        async with new_session() as session:
            request = select(SessionOrm)
            result = await session.execute(request)
            session_models = result.scalars().all()
            # session_schemas = [SSession.model_validate(session_model) for session_model in session_models]
            return session_models