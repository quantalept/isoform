from typing import List
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.questions import Questions
from uuid import UUID

class Questions:
    def __init__(self, db:AsyncSession):
        self.db = db

#create 
async def create_question(
        self,
        form_id: UUID,
        question_id: int,
        section_uuid: UUID,
        question_text: dict 
    ):
        try:
            # Assuming `Questions` is your SQLAlchemy model
            new_question = Questions(
                form_id=form_id,
                question_id=question_id,
                section_uuid=section_uuid,
                question_text=question_text
            )

            self.db.add(new_question)
            await self.db.commit()
            await self.db.refresh(new_question)
            return new_question

        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error while creating question: {str(e)}")
    

#read
#all
async def get_questions(self, skip: int = 0, limit: int = 100):
        query = select(Questions).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

#update

async def update_question(self,
    db:AsyncSession, 
    question_id: int, 
    form_id:UUID = None,
    section_uuid:UUID = None, 
    question_text:dict =None,
    is_required:bool = None,
    order:int= None):
    
    try:
        question = self.db.query(Questions).filter(Questions.question_id == question_id).first()
        if not question:
            raise ValueError(f"Question {question_id} not found.")
        
        if form_id is not None:
            question.form_id = form_id
        if section_uuid is not None:
            question.section_uuid = section_uuid
        if question_text is not None:
            question.question_text = question_text
        if is_required is not None:
            question.is_required = is_required
        if order is not None:
            question.order = order

        await db.commit()
        await db.refresh(question)
        return question
        
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error :{str(e)}")


    except Exception as e:
        raise RuntimeError(f"Error!: {str(e)}")
    
#delete

async def delete_question(self,db:AsyncSession,question_id: int):
    try:
        question = self.db.query(Questions).filter(Questions.question_id == question_id).first()
        if not question:
            raise ValueError(f"Question {question_id} not found.")
        await db.delete(question)
        await db.commit()
    
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError (f"Databasr error while deleting :{str(e)}")
    
