from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    user_id: int
    question: str
    dialog_id: Optional[int] = None  # если не передан, создадим новый диалог

class QueryResponse(BaseModel):
    id: str
    text: str
    sender: str