from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.schemas.sections import SectionCreate, SectionUpdate, SectionRead
from app.models.sections import Sections as SectionModel


class Section:
    def __init__(self, db: AsyncSession):
        self.db = db

async def create_section(self, section_data: SectionCreate):
        try:
            new_section = SectionModel(**section_data.model_dump())
            self.db.add(new_section)
            await self.db.commit()
            await self.db.refresh(new_section)
            return new_section

        except SQLAlchemyError as e:
            if self.db.is_active:
                await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

        except Exception as e:
            if self.db.is_active:
                await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
        
            
async def read_sections(self,
        db:AsyncSession, 
        form_id:UUID, 
        section_id:int, 
        section_name:str,
        section_order:int,
        section_UUID:UUID,
        section_description:str, 

    ):
        try:
            new_section = Section(
                form_id=form_id,
                section_id=section_id, 
                section_name=section_name,
                section_order=section_order,
                section_UUID=section_UUID,
                section_description=section_description)

            self.db.add(new_section)
            await self.db.commit()
            await self.db.refresh(new_section)
            return new_section
        except Exception as e:
            raise HTTPException(status_code=404, detail="Section not found")      
          
async def get_all_sections(self):
        try:
            result = await self.db.execute(select(Section))
            sections = result.scalars().all()

            if not sections:
                raise HTTPException(status_code=404, detail="No sections found")

            return sections

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        

async def update_section(self, section_uuid: UUID, section_data: SectionUpdate):
    section = await self.db.get(SectionModel, section_uuid)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")

    update_data = section_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(section, key, value)

    await self.db.commit()
    await self.db.refresh(section)
    return section

async def delete_section(self, section_id: UUID):
        try:
            result = await self.db.execute(select(Section).filter(Section.id == section_id))
            section = result.scalars().first()

            if not section:
                raise HTTPException(status_code=404, detail="Section not found")
            await self.db.delete(section)
            await self.db.commit()

            return {"detail": "Section deleted successfully"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
