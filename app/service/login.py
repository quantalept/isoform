import bcrypt
from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.schemas.login import UserResponse, LoginRequest
from app.models.admin_user import AdminUserModel

router = APIRouter()

@router.post("/login", response_model=UserResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        valid = validate_email(request.email)
        email = valid.email
    except EmailNotValidError:
        raise HTTPException(status_code=400, detail="Invalid email format")

    result = await db.execute(select(AdminUserModel).filter(AdminUserModel.email == email))
    user = result.scalars().first()

    if user is None or not bcrypt.checkpw(request.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return UserResponse(
        admin_user_id=user.admin_user_id,
        email=user.email,
        username=user.username
    )

