from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.admin_user import AdminUserService
from fastapi import HTTPException
from uuid import UUID
from app.schemas.admin_user import AdminUserCreateDTO, AdminUserResponseDTO

router = APIRouter()

@router.get("/admin_users/{email}", response_model=AdminUserResponseDTO)
async def get_admin_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    admin_user_service = AdminUserService(db)
    admin_user = await admin_user_service.get_admin_user_by_mail(email=email)
    if not admin_user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    return admin_user

@router.get("/admin_users/", response_model=list[AdminUserResponseDTO])
async def get_admin_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    admin_user_service = AdminUserService(db)
    return await admin_user_service.get_admin_users(skip=skip, limit=limit)

@router.post("/admin_users/", response_model=AdminUserResponseDTO)
async def create_admin_user(admin_user: AdminUserCreateDTO, db: AsyncSession = Depends(get_db)):
    admin_user_service = AdminUserService(db)
    return await admin_user_service.create_admin_user(admin_user=admin_user)

@router.put("/admin_users/{admin_user_id}", response_model=AdminUserResponseDTO)
async def update_admin_user(admin_user_id: UUID, admin_user: AdminUserCreateDTO, db: AsyncSession = Depends(get_db)):
    admin_user_service = AdminUserService(db)
    updated_user = await admin_user_service.update_admin_user(admin_user_id=admin_user_id, admin_user=admin_user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    return updated_user
