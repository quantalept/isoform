# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.future import select
from app.api import admin_user,questions,forms

app = FastAPI()

@app.get("/users")
async def read_users(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

app.include_router(admin_user.router, prefix="/forms", tags=["Users"])
app.include_router(forms.router, prefix="/forms", tags=["Forms"])
app.include_router(questions.router, prefix="/forms", tags=["Questions"])
