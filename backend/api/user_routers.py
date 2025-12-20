from fastapi import APIRouter, Depends
from typing import Annotated
from backend.models.user_schemas import SUserAdd, SUser
from backend.database.repository import UserRepository


user_router = APIRouter(
    prefix="/users"
)

@user_router.post("")
async def add_user(
    user: Annotated[SUserAdd, Depends()],
):
    user_id = await UserRepository.add_one(user)
    return {"ok": True, "user_id": user_id}

@user_router.get("")
async def get_users() -> list[SUser]:
    users = await UserRepository.find_all()
    return users