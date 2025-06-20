from pydantic import BaseModel, UUID4


class SectionBase(BaseModel):
    form_id: UUID4
    section_id: int
    section_name: str
    section_order: int | None = None
    section_description: str | None = None

class SectionCreate(SectionBase):
    pass

class Section(SectionBase):
    section_uuid: UUID4

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            'form_id': 'formId',
            'section_id': 'sectionId',
            'section_uuid': 'sectionUuid',
            'section_name': 'sectionName',
            'section_order': 'sectionOrder',
            'section_description': 'sectionDescription'
        }

class SectionUpdate(BaseModel):
    section_name: str | None = None
    section_order: int | None = None
    section_description: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            'section_name': 'sectionName',
            'section_order': 'sectionOrder',
            'section_description': 'sectionDescription'
        }