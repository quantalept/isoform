from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.questions import QuestionCreateDTO, QuestionUpdateDTO, QuestionResponseDTO
from app.crud.questions import Questions

router = APIRouter()

@router.post("/questions/{question.id}")
async def create_question(question_id: str, db: Session = Depends(get_db)):
    questions= Questions(db)
    return await questions.create_question(question_id=question_id)

@router.get("/question/")
async def read_all_questions(question_id: str, db: Session = Depends(get_db)):
    questions = Questions(db)
    return await questions.read_all_questions(question_id=question_id)


@router.put("/questions/{question_id}", response_model=QuestionResponseDTO)
async def update_question(question_id: str, db: Session = Depends(get_db)):
    questions = Questions(db)
    return await questions.update_question(question_id= question_id, update_question=update_question)

@router.delete("/questions/{question_id}")
async def delete_question(question_id: str, db: Session = Depends(get_db)):
    question = Questions(db)
    Question = question.create_question(question_id= question_id)
    if not Question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    await db.delete(question)
    await db.commit()