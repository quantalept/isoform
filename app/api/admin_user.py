from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.admin_user import AdminUserCreateDTO, AdminUserUpdateDTO

router = APIRouter()
@router.get("/admin_users/{email}")
async def get_admin_user_by_email(email: str, db: Session = Depends(get_db)):
    from app.crud.admin_user import AdminUserService
    admin_user_service = AdminUserService(db)
    return admin_user_service.get_admin_user_by_mail(email=email)

@router.get("/admin_users/")
async def get_admin_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    from app.crud.admin_user import AdminUserService
    admin_user_service = AdminUserService(db)
    return await admin_user_service.get_admin_users(skip=skip, limit=limit)

@router.post("/admin_users/")
async def create_admin_user(admin_user: AdminUserCreateDTO, db: Session = Depends(get_db)):
    from app.crud.admin_user import AdminUserService
    admin_user_service = AdminUserService(db)
    return await admin_user_service.create_admin_user(admin_user=admin_user)

@router.put("/admin_users/{admin_user_id}")
async def update_admin_user(admin_user_id: int, admin_user: dict, db: Session = Depends(get_db)):
    from app.crud.admin_user import AdminUserService
    admin_user_service = AdminUserService(db)
    return await admin_user_service.update_admin_user(admin_user_id=admin_user_id, admin_user=admin_user)