from pydantic import BaseModel,UUID4

class FormBase(BaseModel):
    
    form_name: str
    form_description: str
    form_type: str
    form_created_by: UUID4

class FormCreateDTO(FormBase):
    pass

class FormUpdateDTO(BaseModel):
    form_name: str | None = None
    form_description: str | None = None
    form_type: str | None = None
    form_created_by: UUID4 | None = None

class FormResponseDTO(FormBase):
    form_id: UUID4

    class Config:
        orm_mode = True