from fastapi import APIRouter, Depends  
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.crud.user import UserCRUD  # Class-based CRUD



router = APIRouter()

@router.post("/users/", response_model=UserOut)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserCRUD(db)  # Initialize the class with db session
    return user_service.create(user=user)  

@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserCRUD(db)
    return user_service.get(user_id=user_id)

@router.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    user_service = UserCRUD(db)
    return user_service.get_all()

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserCRUD(db)
    return user_service.update(user_id=user_id, user=user)

@router.delete("/users/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserCRUD(db)
    return user_service.delete(user_id=user_id)