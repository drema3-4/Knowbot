from pydantic import BaseModel
from typing import Optional, List

class UploadResponse(BaseModel):
    message: str
    task_id: Optional[str] = None
    processed_files: Optional[List[str]] = None

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    id: str
    text: str
    sender: str