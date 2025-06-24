from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
from app.models.forms import FormsModel
from app.schemas.forms import FormCreateDTO, FormResponseDTO,FormUpdateDTO
from email_validator import validate_email,EmailNotValidError
import bcrypt


class FormsService:
    def __init__(self, db: Session):
        self.db = db

    async def get_form_by_id(self, form_id: UUID) -> Optional[FormResponseDTO]:
        query = select(FormsModel).where(FormsModel.form_id == form_id)
        result = await self.db.execute(query).scalar_one_or_none()
        form_= result
        if not form_:
            raise HTTPException(status_code=404, detail="Form not found")
        return form_

    async def get_forms(self, skip: int = 0, limit: int = 100) -> List[FormResponseDTO]:
        query = select(FormsModel).offset(skip).limit(limit)
        result = await self.db.execute(query)
        forms = result.scalars().all()
        return [(form) for form in forms]
    
