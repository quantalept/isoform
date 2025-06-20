from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.schemas.answers import AnswerCreateDTO, AnswerUpdateDTO, AnswerResponseDTO
from app.crud.answers import Answer
from uuid import UUID   

router = APIRouter()

@router.post("/answers/", response_model=AnswerResponseDTO, status_code=201)
async def create_answer(
    new_answer: AnswerCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    try:
        answer = Answer(**new_answer.model_dump())
        db.add(answer)
        await db.commit()
        await db.refresh(answer)
        return answer  
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/answers/{answer_id}", response_model=AnswerResponseDTO)
async def read_answer(answer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Answer).filter(Answer.id == answer_id))
    answer = result.scalar_one_or_none()

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    return answer

@router.put("/answers/{answer_id}", response_model=AnswerResponseDTO)
async def update_answer(
    answer_id: int,
    new_answer: AnswerUpdateDTO, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Answer).filter(Answer.id == answer_id))
    answer = result.scalar_one_or_none()

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    update_fields = new_answer.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(answer, key, value)

    try:
        await db.commit()
        await db.refresh(answer)
        return answer
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/answers/")
async def delete_answer(answer_id: int, db: AsyncSession = Depends(get_db)):
    from app.crud.answers import Answer
    answer = Answer(db)
    answer = answer.delete_answer(answer_id= answer_id)
    
    await db.delete(answer)
    await db.commit()
    return {"detail": "Answer deleted successfully"}