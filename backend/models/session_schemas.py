from pydantic import BaseModel


class SSessionAdd(BaseModel):
    user_id: int

class SSession(SSessionAdd):
    session_id: int

class SSessionId(BaseModel):
    ok: bool
    session_id: int