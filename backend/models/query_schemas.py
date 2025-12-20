from pydantic import BaseModel


class SQueryAdd(BaseModel):
    session_id: int
    num_query_in_session: int
    query: str

class SQuery(SQueryAdd):
    query_id: int

class SQueryId(BaseModel):
    ok: bool
    query_id: int