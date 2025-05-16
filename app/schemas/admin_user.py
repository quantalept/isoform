from pydantic import BaseModel, EmailStr,UUID4
from typing import Optional

class AdminUserBaseDTO(BaseModel):
    username: str
    email: EmailStr
    phone_number: Optional[str] = None

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
        orm_mode = True