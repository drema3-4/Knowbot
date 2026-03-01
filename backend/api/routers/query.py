from fastapi import APIRouter, Depends, HTTPException

from schemas.query import QueryRequest, QueryResponse
from api.dependencies import (
    get_rag_engine,
    get_user_repository,
    get_dialog_repository,
    get_message_repository
)
from services.rag_engine import RAGEngine
from db.repositories.user_repository import UserRepository
from db.repositories.dialog_repository import DialogRepository
from db.repositories.message_repository import MessageRepository

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    rag_engine: RAGEngine = Depends(get_rag_engine),
    user_repo: UserRepository = Depends(get_user_repository),
    dialog_repo: DialogRepository = Depends(get_dialog_repository),
    message_repo: MessageRepository = Depends(get_message_repository)
):
    # 1. Проверяем, существует ли пользователь
    user = await user_repo.get_user_by_id(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Определяем dialog_id (создаём новый, если не передан)
    dialog_id = request.dialog_id
    if not dialog_id:
        new_dialog = await dialog_repo.add_dialog(request.user_id)
        dialog_id = new_dialog.dialog_id
    else:
        # Если dialog_id передан, проверяем, что диалог принадлежит пользователю
        dialog = await dialog_repo.get_dialog_by_id(dialog_id)
        if not dialog or dialog.user_id != request.user_id:
            raise HTTPException(status_code=403, detail="Dialog not found or access denied")

    # 3. Сохраняем сообщение пользователя
    await message_repo.add_message(
        user_id=request.user_id,
        dialog_id=dialog_id,
        content=request.question,
        role="user"
    )

    # 4. Получаем ответ от RAG
    try:
        answer = rag_engine.query(request.question)
    except Exception as e:
        # В случае ошибки RAG, можно сохранить ошибку или просто пробросить исключение
        raise HTTPException(status_code=500, detail=f"RAG error: {str(e)}")

    # 5. Сохраняем ответ ассистента
    assistant_message = await message_repo.add_message(
        user_id=request.user_id,
        dialog_id=dialog_id,
        content=answer,
        role="assistant"
    )

    # 6. Возвращаем ответ
    return QueryResponse(
        id=str(assistant_message.message_id),
        text=answer,
        sender="bot",
        dialog_id=dialog_id
    )