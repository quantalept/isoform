from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime 
from app.db.base import Base
import uuid
from sqlalchemy.orm import relationship


class FormsModel(Base):
    __tablename__ = "forms"

    form_id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4, index=True)
    form_name = Column(String, unique=True, nullable=False)
    form_description = Column(String, nullable=False)
    form_type = Column(String, nullable=False)
    form_created_at = Column(DateTime, default=datetime.now, nullable=False)
    form_updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    form_created_by = Column(UUID(as_uuid=True),ForeignKey('admin_user.admin_user_id'), nullable=False)

    admin_user = relationship("AdminUserModel", back_populates="forms")
    questions = relationship("Questions", back_populates="form")
    logics = relationship("Logic", back_populates="form", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="form", cascade="all, delete-orphan")
    sections = relationship("Sections", back_populates="form", cascade="all, delete-orphan")
