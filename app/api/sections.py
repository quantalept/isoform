from typing import List, Optional
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.section import Section
from app.schemas.sections import SectionCreate, SectionUpdate, Section
from uuid import UUID

router = APIRouter()


@router.post("/sections/", response_model=Section, status_code=201)
async def create_section(
    section_data: Section,
    db: AsyncSession = Depends(get_db)
):
    new_section = Section(**section_data.model_dump())
    db.add(new_section)
    await db.commit()
    await db.refresh(new_section)
    return new_section


@router.get("/sections/", response_model=List[Section])
async def read_sections(
    form_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Section)
    if form_id:
        query = query.filter(Section.form_id == form_id)

    result = await db.execute(query)
    return result.scalars().all()

@router.put("/sections/{section_id}", response_model=Section)
async def update_section(
    section_id: int,
    section_data: Section,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Section).filter(Section.section_id == section_id))
    section = result.scalar_one_or_none()

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    for key, value in section_data.model_dump(exclude_unset=True).items():
        setattr(section, key, value)

    await db.commit()
    await db.refresh(section)
    return section

@router.delete("/sections/{section_id}", status_code=204)
async def delete_section(section_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Section).filter(Section.section_id == section_id))
    section = result.scalar_one_or_none()

    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    await db.delete(section)
    await db.commit()
    return 
