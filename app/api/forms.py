from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models import FormsModel
from app.crud.forms import FormsService
from app.schemas.forms import FormCreateDTO, FormResponseDTO , FormUpdateDTO
from app.crud.forms import get_forms_by_user_id

router = APIRouter()

@router.get("/forms/{form_id}", response_model=FormResponseDTO)
async def get_form_by_id(form_id: UUID, db: AsyncSession = Depends(get_db)):
    form_service = FormsService(db)
    form = await form_service.get_form_by_id(form_id)
    return form

@router.get("/forms/", response_model=list[FormResponseDTO])
async def get_forms(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    form_service = FormsService(db)
    return await form_service.get_forms(skip=skip, limit=limit)

@router.post("/forms/", response_model=FormResponseDTO)
async def create_form(form: FormCreateDTO, db: AsyncSession = Depends(get_db)):
    form_service = FormsService(db)
    return await form_service.create_form(form_data=form)

@router.put("/forms/{form_id}", response_model=FormResponseDTO)
async def update_form(form_id: str, form: FormUpdateDTO, db: AsyncSession = Depends(get_db)):
    form_service = FormsService(db)
    return await form_service.update_form(form_id=form_id, form=form)

@router.delete("/forms/{form_id}", response_model=dict)
async def delete_form(form_id: str, db: AsyncSession = Depends(get_db)):
    form_service = FormsService(db)
    await form_service.delete_form(form_id=form_id)
    return {"message": "Form deleted successfully"}

@router.get("/users/{user_id}/forms", response_model=List[FormResponseDTO])
async def get_forms_by_admin_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db)
):
    forms = await get_forms_by_user_id(user_id, session)
    return forms