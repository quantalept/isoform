from pydantic import BaseModel, UUID4,field_validator
from typing import Optional, List,Any
from app.utils.validation import validate_answer_type

class AnswerBaseDTO(BaseModel):
    question_id: int
    answer_text: Any
    response_id: int

class AnswerCreateDTO(BaseModel):
    question_id: int
    answer_text: Any
    response_id: int
    question_type: str

    @field_validator("answer_text")
    @classmethod
    def check_answer(cls, v, values):
        qtype = values.data.get("question_type")
        return validate_answer_type(v, qtype)

class AnswerUpdateDTO(BaseModel):
    question_id: Optional[int] = None
    answer_text: Optional[Any] = None
    response_id: Optional[int] = None

class AnswerResponseDTO(AnswerBaseDTO):
    answer_id: UUID4

    class Config:
        orm_mode = True

