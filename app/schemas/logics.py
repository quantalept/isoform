from pydantic import BaseModel,UUID4

class LogicBase(BaseModel):
    form_id: UUID4
    source_question_id: int
    operator: str
    target_question_id: int | None = None
    target_section_uuid: UUID4 | None = None
    value: str

class LogicCreateDTO(LogicBase):
    pass

class LogicUpdateDTO(BaseModel):
    form_id: UUID4 | None = None
    source_question_id: int | None = None
    operator: str | None = None
    target_question_id: int | None = None
    target_section_uuid: UUID4 | None = None
    value: str | None = None

class LogicResponseDTO(LogicBase):
    logic_id: UUID4

    class Config:
        orm_mode = True
        