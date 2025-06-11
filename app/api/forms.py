from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.forms import FormCreateDTO, FormUpdateDTO, FormResponseDTO
from app.crud.forms import FormService

router = APIRouter()

@router.get("/forms/{form_id}", response_model=FormResponseDTO)
def get_form_by_id(form_id: str, db: Session = Depends(get_db)):
    form_service = FormService(db)
    return form_service.get_form_by_id(form_id=form_id)

@router.get("/forms/", response_model=list[FormResponseDTO])
def get_forms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    form_service = FormService(db)
    return form_service.get_forms(skip=skip, limit=limit)

@router.post("/forms/", response_model=FormResponseDTO)
def create_form(form: FormCreateDTO, db: Session = Depends(get_db)):
    form_service = FormService(db)
    return form_service.create_form(form=form)

@router.put("/forms/{form_id}", response_model=FormResponseDTO)
def update_form(form_id: str, form_update: FormUpdateDTO, db: Session = Depends(get_db)):
    form_service = FormService(db)
    return form_service.update_form(form_id=form_id, form_update=form_update)

@router.delete("/forms/{form_id}")
def delete_form(form_id: str, db: Session = Depends(get_db)):
    form_service = FormService(db)
    form = form_service.get_form_by_id(form_id=form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form not found")
    
    db.delete(form)
    db.commit()
    return {"detail": "Form deleted successfully"}