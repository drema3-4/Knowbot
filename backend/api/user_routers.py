from fastapi import APIRouter, Depends
from typing import Annotated
from models.user_schemas import SUserAdd, SUser, SUserId
from database.user_repository import UserRepository


user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.post("")
async def add_user(
    user: Annotated[SUserAdd, Depends()],
) -> SUserId:
    user_id = await UserRepository.add_one()
    return {"ok": True, "user_id": user_id}

@user_router.get("")
async def get_users() -> list[SUser]:
    users = await UserRepository.find_all()
    return users