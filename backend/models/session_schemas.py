from pydantic import BaseModel


class SSessionAdd(BaseModel):
    user_id: int

class SSession(SSessionAdd):
    session_id: int   