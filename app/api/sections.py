from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.models.sections import Sections as SectionModel
from app.crud.section import Section as SectionService
from app.schemas.sections import SectionCreate, SectionUpdate, SectionRead  # Pydantic schemas
from uuid import UUID

router = APIRouter()

@router.post("/sections/", response_model=SectionRead, status_code=201)
async def create_section(
    section_data: SectionCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        new_section = SectionModel(**section_data.model_dump())
        db.add(new_section)
        await db.commit()
        await db.refresh(new_section)
        return new_section

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/sections/", response_model=List[SectionRead])
async def read_sections(
    form_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(SectionModel)  # NOT SectionService or anything else
    if form_id:
        query = query.filter(SectionModel.form_id == form_id)

    result = await db.execute(query)
    return result.scalars().all()


@router.put("/sections/{section_uuid}", response_model=SectionRead)
async def update_section(
    section_uuid: UUID,
    section_data: SectionUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = SectionService(db)
    updated_section = await service.update_section(section_uuid, section_data)
    return updated_section


@router.delete("/sections/{section_id}", status_code=204)
async def delete_section(section_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SectionService).filter(SectionService.section_id == section_id))
    section = result.scalar_one_or_none()

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    await db.delete(section)
    await db.commit()
    return
