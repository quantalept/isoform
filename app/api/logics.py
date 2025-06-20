from typing import List
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import get_db
from app.crud.logics import Logics
from app.schemas.logics import LogicCreateDTO, LogicUpdateDTO, LogicResponseDTO
from uuid import UUID

router = APIRouter()
async def get_logic_service(db: AsyncSession = Depends(get_db)):
    return Logics(db)

@router.post("/logic/", response_model=LogicResponseDTO, status_code=201)
async def create_logic(
    logic_data: LogicCreateDTO,
    db: AsyncSession = Depends(get_db)
):
    new_logic = Logics(**logic_data.model_dump())

    db.add(new_logic)
    try:
        await db.commit()
        await db.refresh(new_logic)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    return new_logic
        

@router.put("/logic/{logic_id}", response_model=LogicUpdateDTO)
async def update_logic(
    logic_id: UUID,
    logic_data: LogicUpdateDTO,
    service: Logics = Depends(get_logic_service)  
):
    updated_logic = await service.update_logic(logic_id, logic_data)
    if not updated_logic:
        raise HTTPException(status_code=404, detail="Logic not found")
    return updated_logic


@router.put("/{logic_id}", response_model=LogicUpdateDTO)
async def update_logic(
    logic_id: UUID,
    logic_data: LogicUpdateDTO,
    service: Logics = Depends(get_db)
):  
    from app.crud.logics import Logic       
    logic = await service.update_logic(logic_id, logic_data)
    if not logic:
        raise HTTPException(status_code=404, detail="Logic not found")
    return logic


@router.delete("/{logic_id}")
async def delete_logic(
    logic_id: UUID,
    service: Logics = Depends(get_db)
):
    from app.crud.logics import Logic   
    deleted = await service.delete_logic(logic_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Logic not found")
    return