from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
from app.models.forms import FormsModel
from app.schemas.forms import FormCreateDTO, FormUpdateDTO, FormResponseDTO

class FormService:
    def __init__(self, db: Session):
        self.db = db

    async def get_form_by_id(self, form_id: UUID) -> FormResponseDTO:
        form =await self.db.query(FormsModel).filter(FormsModel.form_id == form_id).first()
        if not form:
            raise HTTPException(status_code=404, detail="Form not found")
        return form

    async def get_forms(self, skip: int = 0, limit: int = 100) :
        return await self.db.query(FormsModel).offset(skip).limit(limit).all()

    async def create_form(self, form: FormCreateDTO) -> FormResponseDTO:
        db_form = FormsModel(
            form_name=form.form_name,
            form_description=form.form_description,
            form_type=form.form_type,
            form_created_by=form.form_created_by
        )
        self.db.add(db_form)
        self.db.commit()
        self.db.refresh(db_form)
        return db_form

    async def update_form(self, form_id: UUID, form_update: FormUpdateDTO) -> FormResponseDTO:
        db_form = self.get_form_by_id(form_id)
        if not db_form:
            raise HTTPException(status_code=404, detail="Form not found")

        for key, value in form_update.dict(exclude_unset=True).items():
            setattr(db_form, key, value)

        self.db.commit()
        self.db.refresh(db_form)
        return db_form