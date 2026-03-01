from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from services.rag_engine import RAGEngine
from services.vector_store_service import VectorStoreService
from db.session import get_db
from db.repositories.user_repository import UserRepository
from db.repositories.dialog_repository import DialogRepository
from db.repositories.message_repository import MessageRepository


def get_rag_engine(request: Request) -> RAGEngine:
    return request.app.state.rag_engine

def get_vector_store_service(request: Request) -> VectorStoreService:
    return request.app.state.vector_store_service


async def get_user_repository(
    session: AsyncSession = Depends(get_db)
) -> UserRepository:
    return UserRepository(session)

async def get_dialog_repository(
    session: AsyncSession = Depends(get_db)
) -> DialogRepository:
    return DialogRepository(session)

async def get_message_repository(
    session: AsyncSession = Depends(get_db)
) -> MessageRepository:
    return MessageRepository(session)