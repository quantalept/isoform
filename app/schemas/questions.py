from pydantic import BaseModel, UUID4

class QuestionBase(BaseModel):
    section_uuid: UUID4
    question_text: str
    question_type: str
    is_required: bool
    order: int

class QuestionCreateDTO(QuestionBase):
    pass

class QuestionUpdateDTO(BaseModel):
    question_text: str | None = None
    question_type: str | None = None
    is_required: bool | None = None
    order: int | None = None
    section_uuid: UUID4 | None = None

class QuestionResponseDTO(QuestionBase):
    question_id: int



    class Config:
        orm_mode = True
        use_enum_values = True  # If you want to return enum values instead of names

