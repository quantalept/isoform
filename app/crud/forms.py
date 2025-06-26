from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
from app.models.forms import FormsModel
from app.schemas.forms import FormCreateDTO, FormResponseDTO,FormUpdateDTO
from email_validator import validate_email,EmailNotValidError
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt


class FormsService:
    def __init__(self, db: Session):
        self.db = db

    async def get_form_by_id(self, form_id: UUID) -> FormsModel:
        query = select(FormsModel).where(FormsModel.form_id == form_id)
        result = await self.db.execute(query)
        form_ = result.scalar_one_or_none()
        if not form_:
            raise HTTPException(status_code=404, detail="Form not found")
        return form_

    async def get_forms(self, skip: int = 0, limit: int = 100) -> List[FormResponseDTO]:
        query = select(FormsModel).offset(skip).limit(limit)
        result = await self.db.execute(query)
        forms = result.scalars().all()
        return [(form) for form in forms]
    
    
    async def create_form(self, form_data: FormCreateDTO) -> FormResponseDTO:
        created_form = FormsModel(
            form_name=form_data.form_name,
            form_description=form_data.form_description,
            form_type=form_data.form_type,
            form_created_by=form_data.form_created_by
        )

        self.db.add(created_form)
        await self.db.commit()
        await self.db.refresh(created_form)
        return created_form

    async def update_form(self,
        form:FormUpdateDTO,
        form_id: str
    ) -> FormsModel:
        # Fetch the existing form by ID
        form_1 = await self.db.get(FormsModel, form_id)
        if not form_1:
            raise ValueError(f"Form with id {form_id} not found")
        if form.form_name:
            form_1.form_name =form.form_name      
        if form.form_description:
            form_1.form_description = form.form_description
        if form.form_type:
            form_1.form_type= form.form_type

        await self.db.commit()
        await self.db.refresh(form_1)
        return form_1

    async def delete_form(self, form_id: str) -> None:
        # Fetch the form by ID
        form = await self.db.get(FormsModel, form_id)
        if not form:
            raise ValueError(f"Form with id {form_id} not found")

        await self.db.delete(form)
        await self.db.commit()

    
async def get_forms_by_user_id(user_id: UUID, session: AsyncSession) -> List[FormsModel]:
    result = await session.execute(
        select(FormsModel).where(FormsModel.form_created_by == user_id)
    )
    return result.scalars().all()