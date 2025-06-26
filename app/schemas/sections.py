from pydantic import BaseModel, UUID4


class SectionBase(BaseModel):
    form_id: UUID4
    section_id: int
    section_name: str
    section_order: int | None = None 
    section_description: str | None = None

class SectionCreate(SectionBase):
    pass

class SectionRead(SectionBase):
    section_uuid: UUID4

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class SectionUpdate(BaseModel):
    section_name: str | None = None
    section_order: int | None = None
    section_description: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        