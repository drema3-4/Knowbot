from fastapi import APIRouter, Depends
from typing import Annotated
from backend.models.user_schemas import SAnswerAdd, SAnswer
from repository import AnswerRepository


answer_router = APIRouter(
    prefix="/answers"
)

@answer_router.post("")
async def add_answer(
    answer: Annotated[SAnswerAdd, Depends()],
):
    answer_id = await AnswerRepository.add_one(answer)
    return {"ok": True, "answer_id": answer_id}

@answer_router.get("")
async def get_answers() -> list[SAnswer]:
    answers = await AnswerRepository.find_all()
    return answers