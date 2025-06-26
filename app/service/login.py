import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.login import UserResponse, LoginRequest
from app.models.admin_user import AdminUserModel
from sqlalchemy.future import select


async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        valid = validate_email(request.Email)
        email = valid.email
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Invalid email format")

    result = await db.execute(select(AdminUserModel).filter(AdminUserModel.email == email))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(request.Password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return UserResponse(
    admin_user_id=user.admin_user_id,
    email=user.email,
    username=user.username
)
