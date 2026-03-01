from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    user_name: str

class UserResponse(BaseModel):
    user_id: int
    user_name: str