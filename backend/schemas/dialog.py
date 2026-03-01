from pydantic import BaseModel
from datetime import datetime


class DialogCreateRequest(BaseModel):
    user_id: int

class DialogResponse(BaseModel):
    dialog_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # позволяет конвертировать SQLAlchemy модель в Pydantic