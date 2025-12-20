from pydantic import BaseModel


class SAnswerAdd(BaseModel):
    session_id: int
    num_answer_in_session: int
    answer: str

class SAnswer(SAnswerAdd):
    answer_id: int