from fastapi import APIRouter, Depends
from typing import Annotated
from models.session_schemas import SSessionAdd, SSession, SSessionId
from database.session_repository import SessionRepository


session_router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

@session_router.post("")
async def add_session(
    session: Annotated[SSessionAdd, Depends()],
) -> SSessionId:
    session_id = await SessionRepository.add_one(session)
    return {"ok": True, "session_id": session_id}

@session_router.get("")
async def get_sessions() -> list[SSession]:
    sessions = await SessionRepository.find_all()
    return sessions