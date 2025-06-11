from uuid import UUID
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
from app.models.admin_user import AdminUserModel
from app.schemas.admin_user import AdminUserCreateDTO, AdminUserUpdateDTO
from email_validator import validate_email,EmailNotValidError
import bcrypt


class AdminUserService:
    def __init__(self, db: Session):
        self.db = db

    def get_admin_user_by_mail(self, email: str):
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail=f"Invalid email: {e}")
        
        result = self.db.query(AdminUserModel.admin_user_id, AdminUserModel.username).filter(AdminUserModel.email == email).first()
        if not result:
            raise HTTPException(status_code=404, detail="Admin user not found")
        return {"admin_user_id": str(result.admin_user_id), "username": result.username}

    def get_admin_users(self, skip: int = 0, limit: int = 100) -> List[AdminUserModel]:
        return self.db.query(AdminUserModel).offset(skip).limit(limit).all()

    def create_admin_user(self, admin_user: AdminUserCreateDTO) -> AdminUserModel:
        try:
            validate_email(admin_user.email)
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail=f"Invalid email: {e}")
        
        existing_user = self.db.query(AdminUserModel).filter(
            (AdminUserModel.email == admin_user.email) 
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        hashed_password = bcrypt.hashpw(admin_user.password.encode('utf-8'), bcrypt.gensalt())

        

        db_admin_user = AdminUserModel(
            email=admin_user.email,
            hashed_password=hashed_password.decode('utf-8'),
            username=admin_user.username
        )
        self.db.add(db_admin_user)
        self.db.commit()
        self.db.refresh(db_admin_user)
        return db_admin_user