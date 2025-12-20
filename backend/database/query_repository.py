from sqlalchemy import select
from database.database import new_session, QueryOrm
from models.query_schemas import SQuery, SQueryAdd

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
        
    @classmethod
    async def find_all(cls) -> list[SQuery]:
        async with new_session() as session:
            request = select(QueryOrm)
            result = await session.execute(request)
            query_models = result.scalars().all()
            # query_schemas = [SQuery.model_validate(query_model) for query_model in query_models]
            return query_models