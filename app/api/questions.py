from typing import List
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.schemas.questions import QuestionCreateDTO, QuestionUpdateDTO, QuestionResponseDTO
from app.crud.questions import Questions
from uuid import UUID   

router = APIRouter()

@router.post("/question/", response_model=QuestionResponseDTO)
async def create_question(
    new_question: QuestionCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    try:
        question = Questions(**new_question.model_dump())
        db.add(question)
        await db.commit()
        await db.refresh(question)
        return question 
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/question/", response_model=List[QuestionResponseDTO])
async def read_all_questions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Questions).offset(skip).limit(limit))
    questions = result.scalars().all()
    return questions

@router.put("/question/{question_id}", response_model=QuestionResponseDTO)
async def update_question(
    question_id: int,
    new_question: QuestionUpdateDTO, 
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(Questions).filter(Questions.id == question_id))
        question = result.scalar_one_or_none()
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        update_fields = new_question.model_dump(exclude_unset=True)
        for key, value in update_fields.items():
            setattr(question, key, value)

        await db.commit()
        await db.refresh(question)
        return question

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.delete("/question/{question_id}", status_code=204)
async def delete_question(
    question_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Questions).filter(Questions.id == question_id))
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    await db.delete(question)
    await db.commit()
    return  
 