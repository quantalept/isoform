from db.session import engine
from db.base import Base
from models.user import User  # Make sure model is imported

def init_db():
    Base.metadata.create_all(bind=engine)
