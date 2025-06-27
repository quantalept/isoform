from uuid import UUID
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    admin_user_id: UUID
    email: str
    username: str | None = None

    class Config:
        orm_mode = True
