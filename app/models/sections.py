from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Sections(Base):
    __tablename__ = "sections"

    section_uuid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    section_id = Column(Integer, index=True)
    form_id = Column(UUID(as_uuid=True), ForeignKey("forms.form_id"), nullable=False)
    section_name = Column(String, nullable=False)
    section_description = Column(String, nullable=True)
    section_order = Column(Integer, nullable=False)

    # Relationships
    form = relationship("FormsModel", back_populates="sections")
    questions = relationship("Questions", back_populates="section")  # Assuming Questions has a section relationship