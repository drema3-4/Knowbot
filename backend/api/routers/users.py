from fastapi import APIRouter, Depends, HTTPException

from schemas.user import UserResponse, UserCreateRequest
from db.repositories.user_repository import UserRepository
from api.dependencies import get_user_repository


router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse)
async def create_user(
    request: UserCreateRequest,
    user_repo: UserRepository = Depends(get_user_repository)
):
    existing_user = await user_repo.get_user_by_name(request.user_name)
    if existing_user:
        return UserResponse(user_id=existing_user.user_id, user_name=existing_user.user_name)
    
    new_user = await user_repo.add_user(request.user_name)
    return UserResponse(user_id=new_user.user_id, user_name=new_user.user_name)

@router.get("/by-name/{user_name}", response_model=UserResponse)
async def get_user_by_name(
    user_name: str,
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = await user_repo.get_user_by_name(user_name)
    if not user:
        raise HTTPException(404, "User not found")
    return UserResponse(user_id=user.user_id, user_name=user.user_name)