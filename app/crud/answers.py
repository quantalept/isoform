from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import answers
from uuid import UUID

class Answer:
    def __init__(self, db: Session):
        self.db = db

#create
    async def create_answer(self,db:Session,
                     answer_id:int,
                     response_id: int, 
                     question_id: int, 
                     answer_text: dict
    ):
        try:
            new_answer = answers(
                answer_id=UUID(),
                response_id=int,
                question_id=int,
                answer_text=str
            )
            await self.db.add(new_answer)
            await self.db.commit()
            await self.db.refresh(new_answer)
            return new_answer
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Database error while creating :{str(e)}")

#read
    async def read_answer(self, answer_id):
        try:
            return await self.db.query(answers).all()
        except SQLAlchemyError as e:
            raise RuntimeError (f"Database error while fetching all :{str(e)}")
        
#update
    async def update(self, db:Session,
                     answer_id:int,
                     response_id:int= None,
                     question_id:int = None, 
                     answer_text: dict =None):
        try:
            answer = self.db.query(answers).filter(answers.answer_id == answer_id).first()

            if not answer:
                raise ValueError(f"Answer {answer_id} not found.")
            if response_id is not None:
                answer.response_id = response_id
            if response_id is not None:
                answer.response_id = response_id
            if question_id is not None:
                answer.question_id = question_id
            if answer_text is not None:
                answer.answer_text = answer_text
            await self.db.commit()
            await self.db.refresh(answer)
            return answer
        
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError(f"Database error while updating :{str(e)}")
        
#delete
    async def delete_answer(self, db:Session,answer_id:int):
        try:
            answer = self.db.query(answers).filter(answers.answer_id == answer_id).first()
            if not answer:
                raise ValueError(f"Answer {answer_id} not found.")
            await self.db.delete(answer)
            await self.db.commit()
            return answer
        except SQLAlchemyError as e:
            db.rollback()
            raise RuntimeError (f"Databasr error while deleting :{str(e)}")
 

  

