from pydantic import BaseModel, UUID4
from typing import Optional

# Shared base
class FormBase(BaseModel):
    form_name: str
    form_description: str
    form_type: str
    form_created_by: UUID4

# Create input DTO
class FormCreateDTO(FormBase):
    pass

# Update input DTO
class FormUpdateDTO(BaseModel):
    form_name: Optional[str] = None
    form_description: Optional[str] = None
    form_type: Optional[str] = None

# Response DTO
class FormResponseDTO(FormBase):
    form_id: UUID4

    class Config:
        orm_mode = True
