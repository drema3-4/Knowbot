from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from schemas.dialog import DialogCreateRequest, DialogResponse
from api.dependencies import get_dialog_repository, get_user_repository, get_message_repository
from db.repositories.dialog_repository import DialogRepository
from db.repositories.user_repository import UserRepository
from schemas.message import MessageResponse
from db.repositories.message_repository import MessageRepository


router = APIRouter(prefix="/dialogs")

@router.get("/user/{user_id}", response_model=List[DialogResponse])
async def get_user_dialogs(
    user_id: int,
    dialog_repo: DialogRepository = Depends(get_dialog_repository)
):
    dialogs = await dialog_repo.get_user_dialogs(user_id)
    return dialogs

@router.post("/", response_model=DialogResponse, status_code=status.HTTP_201_CREATED)
async def create_dialog(
    request: DialogCreateRequest,
    dialog_repo: DialogRepository = Depends(get_dialog_repository),
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = await user_repo.get_user_by_id(request.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_dialog = await dialog_repo.add_dialog(request.user_id)
    return new_dialog

@router.get("/{dialog_id}/messages", response_model=List[MessageResponse])
async def get_dialog_messages(
    dialog_id: int,
    user_id: int = Query(..., description="ID пользователя, которому принадлежит диалог"),
    message_repo: MessageRepository = Depends(get_message_repository)
):
    messages = await message_repo.get_dialog_messages(user_id, dialog_id)
    return messages