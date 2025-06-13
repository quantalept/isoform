from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.answers import AnswerCreateDTO, AnswerUpdateDTO, AnswerResponseDTO
from app.crud.answers import Answer

router = APIRouter()

@router.get("/check_answer/{answer_id}")
async def create_answer(question_id: int, db: Session = Depends(get_db)):
    from app.crud.answers import Answer
    answer= Answer(db)
    return await Answer.create_answer(db=db,answer_id=question_id)

@router.post("/check_answer/")
async def read_answer(question_id: int, answer_text:str,db: Session = Depends(get_db)):
    answer = Answer(db)
    return await answer.read_answer(answer_id=question_id,answer_text=str)


@router.put("/check_answer/{answer_id}", response_model=AnswerUpdateDTO)
async def update_answer(answer_id: int,answer_text:str, db: Session = Depends(get_db)):
    from app.crud.answers import Answer
    answer = Answer(db)
    return await answer.update_answer(answer_id= answer_id, answer_text=str,update_answer=update_answer)

@router.delete("/check_answer/{answer_id}")
async def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    answer = Answer(db)
    answer = answer.delete_answer(answer_id= answer_id)
    
    await db.delete(answer)
    await db.commit()
    return {"detail": "Answer deleted successfully"}