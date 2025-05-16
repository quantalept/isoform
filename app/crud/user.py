from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

class UserCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate):
        db_user = User(email=user.email, full_name=user.full_name)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_full_name(self, full_name: str):
        return self.db.query(User).filter(User.full_name == full_name).first()
    
    def get_all(self):
        return self.db.query(User).all()
    
    def update(self, user_id: int, user: UserCreate):
        db_user = self.get(user_id)
        if db_user:
            db_user.email = user.email
            db_user.full_name = user.full_name
            self.db.commit()
            self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id: int):
        db_user = self.get(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
    


