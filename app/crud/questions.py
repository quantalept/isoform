from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models import questions
from uuid import UUID

class Questions:
    def __init__(self, db:AsyncSession):
        self.db = db

#create 
async def create_question(self,
    db:AsyncSession, 
    form_id:UUID,
    response_id: int, 
    question_id: int, 
    section_uuid:UUID, 
    question_text:dict
  ):
    try:
        new_question = questions(
            form_id = UUID(),
            question_id =int,
            section_uuid = UUID,
            question_text = str,
        )

        self.db.add(new_question)
        await self.db.commit()
        await self.db.refresh(new_question)
        return new_question
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error while creating :{str(e)}")
    

#read
#all
async def read_all_questions(self,db:AsyncSession):
    try:
        return self.db.query(questions).ordre_by().all()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error while fetching all :{str(e)}")

        
#one at time
async def read_questions_ID(self,db:AsyncSession,question_id:int):
    try:
        return self.db.query(questions).filter(questions.question_id == question_id).first()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error while fetching ID :{str(e)}")

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
        question = self.db.query(questions).filter(questions.question_id == question_id).first()
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
        question = self.db.query(questions).filter(questions.question_id == question_id).first()
        if not question:
            raise ValueError(f"Question {question_id} not found.")
        await db.delete(question)
        await db.commit()
    
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError (f"Databasr error while deleting :{str(e)}")
    
