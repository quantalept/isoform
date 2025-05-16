from pydantic import BaseModel, UUID4

class ResponseBase(BaseModel):
    form_id: UUID4
    submitted_at: str

class ResponseCreate(ResponseBase):
    email: str | None = None

class Response(ResponseBase):
    response_id: int
    email: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        fields = {
            'form_id': 'formId',
            'submitted_at': 'submittedAt',
            'response_id': 'responseId'
        }