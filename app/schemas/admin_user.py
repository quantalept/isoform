from pydantic import BaseModel, EmailStr,UUID4
from typing import Optional

class AdminUserBaseDTO(BaseModel):
    username: str
    email: EmailStr
class AdminUserCreateDTO(AdminUserBaseDTO):
    password: str

class AdminUserUpdateDTO(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class AdminUserLoginReqDTO(BaseModel):
    email: EmailStr
    password: str

class AdminUserResponseDTO(AdminUserBaseDTO):
    admin_user_id: UUID4


    class Config:
        from_attributes = True  # For compatibility with SQLAlchemy objects