from pydantic import BaseModel

class SUserAdd(BaseModel):
    pass

class SUser(SUserAdd):
    user_id: int

class SSessionAdd(BaseModel):
    user_id: int

class SSession(SSessionAdd):
    session_id: int    

class SQueryAdd(BaseModel):
    session_id: int
    num_query_in_session: int
    query: str

class SQuery(SQueryAdd):
    query_id: int


class SAnswerAdd(BaseModel):
    session_id: int
    num_answer_in_session: int
    answer: str

class SAnswer(SAnswerAdd):
    answer_id: int