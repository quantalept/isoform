import uuid
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Sections(Base):
    __tablename__ = "sections"

    section_uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    section_id = Column(Integer, index=True, default=0)
    form_id = Column(UUID(as_uuid=True), ForeignKey("forms.form_id"), nullable=False, default=0)
    section_name = Column(String, nullable=False, default=0)
    section_description = Column(String, nullable=True, default=0)
    section_order = Column(Integer, nullable=True, default=0)

    # Relationships
    form = relationship("FormsModel", back_populates="sections")
    questions = relationship("Questions", back_populates="section")  # Assuming Questions has a section relationship
    logics = relationship("Logic", back_populates="section", cascade="all, delete-orphan")