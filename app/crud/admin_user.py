from sqlalchemy import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from fastapi import HTTPException
from app.models.admin_user import AdminUserModel
from app.schemas.admin_user import AdminUserCreateDTO, AdminUserUpdateDTO
from email_validator import validate_email, EmailNotValidError
import bcrypt


class AdminUserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_admin_user_by_mail(self, email: str):
        try:
            validate_email(email)
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail=f"Invalid email: {e}")
        
        query = select(AdminUserModel.admin_user_id, AdminUserModel.username).where(
            AdminUserModel.email == email
        )
        result = await self.db.execute(query)
        user = result.first()

        if not user:
            raise HTTPException(status_code=404, detail="Admin user not found")

        admin_user_id, username = user
        return {
            "admin_user_id": str(admin_user_id),
            "username": username,
            "email": email
        }

    async def get_admin_users(self, skip: int = 0, limit: int = 100):
        query = select(AdminUserModel).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_admin_user(self, admin_user: AdminUserCreateDTO):
        try:
            validate_email(admin_user.email)
        except EmailNotValidError as e:
            raise HTTPException(status_code=400, detail=f"Invalid email: {e}")

        # Check if email already exists
        query = select(AdminUserModel).where(AdminUserModel.email == admin_user.email)
        existing_user = await self.db.execute(query)
        if existing_user.scalars().first():
            raise HTTPException(status_code=400, detail="Email already exists")

        # Hash password
        hashed_password = bcrypt.hashpw(
            admin_user.password.encode('utf-8'),
            bcrypt.gensalt()
        )

        # Create DB entry
        db_admin_user = AdminUserModel(
            email=admin_user.email,
            hashed_password=hashed_password.decode('utf-8'),
            username=admin_user.username
        )

        self.db.add(db_admin_user)
        await self.db.commit()
        await self.db.refresh(db_admin_user)
        return db_admin_user
    
    async def update_admin_user(self, admin_user_id: UUID, admin_user: AdminUserUpdateDTO):
        query = select(AdminUserModel).where(AdminUserModel.admin_user_id == admin_user_id)
        result = await self.db.execute(query)
        db_admin_user = result.scalars().first()

        if not db_admin_user:
            raise HTTPException(status_code=404, detail="Admin user not found")

        if admin_user.username is not None:
            db_admin_user.username = admin_user.username
        if admin_user.email is not None:
            try:
                validate_email(admin_user.email)
                db_admin_user.email = admin_user.email
            except EmailNotValidError as e:
                raise HTTPException(status_code=400, detail=f"Invalid email: {e}")
        if admin_user.password is not None:
            db_admin_user.hashed_password = bcrypt.hashpw(
                admin_user.password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')

        await self.db.commit()
        await self.db.refresh(db_admin_user)
        return db_admin_user
