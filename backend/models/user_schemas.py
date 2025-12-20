from pydantic import BaseModel


class SUserAdd(BaseModel):
    pass

class SUser(SUserAdd):
    user_id: int

class SUserId(BaseModel):
    ok: bool
    user_id: int