from fastapi import APIRouter, Depends
from typing import Annotated
from models.answer_schemas import SAnswerAdd, SAnswer, SAnswerId
from database.answer_repository import AnswerRepository


answer_router = APIRouter(
    prefix="/answers",
    tags=["Answers"]
)

@answer_router.post("")
async def add_answer(
    answer: Annotated[SAnswerAdd, Depends()],
) -> SAnswerId:
    answer_id = await AnswerRepository.add_one(answer)
    return {"ok": True, "answer_id": answer_id}

@answer_router.get("")
async def get_answers() -> list[SAnswer]:
    answers = await AnswerRepository.find_all()
    return answers