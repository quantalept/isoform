from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Logic(Base):
    __tablename__ = "logic"

    logic_id = Column(UUID, primary_key=True, index=True)
    form_id = Column(UUID(as_uuid=True), ForeignKey("forms.form_id"), nullable=False)
    source_question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)
    operator = Column(String, nullable=False)
    target_question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=True)
    target_section_uuid = Column(UUID, ForeignKey("sections.section_uuid"), nullable=True)
    value = Column(String, nullable=False)

    # Relationships
    form = relationship("FormsModel", back_populates="logics")
    source_question = relationship("Questions",foreign_keys=[source_question_id],back_populates="source_logics")
    target_question = relationship("Questions",foreign_keys=[target_question_id],back_populates="target_logics")
    section = relationship("Sections", back_populates="logics")