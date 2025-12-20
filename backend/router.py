from fastapi import APIRouter, Depends
from typing import Annotated

from schemas import SUserAdd, SUser
from repository import UserRepository


router = APIRouter(
    prefix="/users"
)

@router.post("")
async def add_user(
    user: Annotated[SUserAdd, Depends()],
):
    user_id = await UserRepository.add_one(user)
    return {"ok": True, "user_id": user_id}

@router.get("")
async def get_users() -> list[SUser]:
    users = await UserRepository.find_all()
    return users

# @router.post("/query")
# async def add_query(
#     query: Annotated[SQueryAdd, Depends()],
# ):
#     return {"ok": True}

# @router.post("/answer")
# async def add_query(
#     answer: Annotated[SAnswerAdd, Depends()]
# ):
#     return {"ok": True}