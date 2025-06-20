from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from fastapi import HTTPException
from app.models.logics import Logic
from app.schemas.logics import LogicCreateDTO, LogicUpdateDTO, LogicResponseDTO

class Logics:
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def create_answer(self,db:AsyncSession,
        logic_id:UUID,
        form_id: UUID, 
        source_question_id: int, 
        operator: str,
        target_question_id:int,
        target_section_uuid:UUID,
        value:str
                         
                             ):
        try:
            logic = LogicCreateDTO(
                logic_id=logic_id,
                form_id=form_id,
                source_question_id=source_question_id,
                operator=operator,
                target_question_id=target_question_id,
                target_section_uuid=target_section_uuid,
                value=value

            )
            self.db.add(logic)
            await self.db.commit()
            await self.db.refresh(logic)
            return logic
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Database error while creating :{str(e)}")


    async def get_logic_by_id(self, logic_id: UUID):
        try:
            result = await self.db.execute(select(Logic).filter(Logic.logic_id == logic_id))
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error while fetching logic by ID: {str(e)}")

    async def update_logic(self, logic_id: UUID, logic_data: LogicUpdateDTO):
        try:
            logic = await self.get_logic_by_id(logic_id)
            if logic:
                for key, value in logic_data.dict(exclude_unset=True).items():
                    setattr(logic, key, value)
                await self.db.commit()
                await self.db.refresh(logic)
                return logic
            return None
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error while updating logic: {str(e)}")

    async def delete_logic(self, logic_id: UUID) -> bool:
        try:
            logic = await self.get_logic_by_id(logic_id)
            if logic:
                await self.db.delete(logic)
                await self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise RuntimeError(f"Database error while deleting logic: {str(e)}")

    async def get_all_logic(self, skip: int = 0, limit: int = 100) -> List[Logic]:
        try:
            result = await self.db.execute(select(Logic).offset(skip).limit(limit))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error while fetching all logic: {str(e)}")