# database/init_db.py
import asyncio
from db.base import Base
from db.session import engine
from models import user  # make sure all models are imported

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())