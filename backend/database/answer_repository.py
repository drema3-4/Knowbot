from sqlalchemy import select
from database.database import new_session, AnswerOrm
from models.answer_schemas import SAnswer, SAnswerAdd

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
        
    @classmethod
    async def find_all(cls) -> list[SAnswer]:
        async with new_session() as session:
            request = select(AnswerOrm)
            result = await session.execute(request)
            answer_models = result.scalars().all()
            # answer_schemas = [SAnswer.model_validate(answer_model) for answer_model in answer_models]
            return answer_models