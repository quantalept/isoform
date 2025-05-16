from fastapi import APIRouter, Depends  
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.logics import PurchaseCreate, PurchaseOut
from app.crud.purchase import PurchaseCRUD  # Class-based CRUD
from app.service.purchase_service import PurchaseService  # Service layer

router = APIRouter()

@router.post("/purchases/", response_model=PurchaseOut)
def create_new_purchase(purchase: PurchaseCreate, db: Session = Depends(get_db)):
    purchase_service = PurchaseCRUD(db)
    return purchase_service.create(purchase=purchase)

@router.get("/purchases/{purchase_id}", response_model=PurchaseOut)
def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase_service = PurchaseCRUD(db)
    return purchase_service.get(purchase_id=purchase_id)

@router.get("/purchases/")
def get_all_purchases(db: Session = Depends(get_db)):
    purchase_service = PurchaseCRUD(db)
    return purchase_service.get_all()

@router.put("/purchases/{purchase_id}", response_model=PurchaseOut)
def update_purchase(purchase_id: int, purchase: PurchaseCreate, db: Session = Depends(get_db)):
    purchase_service = PurchaseCRUD(db)
    return purchase_service.update(purchase_id=purchase_id, purchase=purchase)

@router.delete("/purchases/{purchase_id}", response_model=PurchaseOut)
def delete_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase_service = PurchaseCRUD(db)
    return purchase_service.delete(purchase_id=purchase_id)

@router.get("/purchases/total/{user_id}")
def get_total_purchase_by_user(user_id: int, db: Session = Depends(get_db)):
    purchase_service = PurchaseService(db)
    return purchase_service.calculate_total_purchase_by_user(user_id=user_id)