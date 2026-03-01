from pydantic import BaseModel
from datetime import datetime


class MessageResponse(BaseModel):
    message_id: int
    dialog_id: int
    user_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True