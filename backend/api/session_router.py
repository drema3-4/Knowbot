from fastapi import APIRouter, Depends
from typing import Annotated
from backend.models.user_schemas import SSessionAdd, SSession
from repository import SessionRepository


session_router = APIRouter(
    prefix="/sessions"
)

@session_router.post("")
async def add_session(
    session: Annotated[SSessionAdd, Depends()],
):
    session_id = await SessionRepository.add_one(session)
    return {"ok": True, "session_id": session_id}

@session_router.get("")
async def get_sessions() -> list[SSession]:
    sessions = await SessionRepository.find_all()
    return sessions