from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base


class AdminUserModel(Base):
    __tablename__ = "admin_user"
    admin_user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String)
    email = Column(String, unique=True, nullable=True)
    phoneNumber = Column(String, unique=True, nullable=True)
    hashedPassword = Column(String)

    forms = relationship("FormsModel", back_populates="admin_user")