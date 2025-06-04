from sqlalchemy import Column, Integer, String,ForeignKey,Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.utils.enums import QuestionType

class Questions(Base):
    __tablename__ = "questions"

    form_id = Column(UUID, ForeignKey("forms.form_id"), nullable=False)
    question_id = Column(Integer, primary_key=True, index=True)
    section_uuid = Column(UUID, ForeignKey("sections.section_uuid"), nullable=False)
    question_text = Column(String, nullable=False)
    question_type = Column(SqlEnum(QuestionType), nullable=False)
    is_required = Column(String, default=False, nullable=False)
    order = Column(Integer, nullable=False)

    # Optional relationships (if you want to easily access related data)
    section = relationship("Sections", back_populates="questions")
    form = relationship("FormsModel", back_populates="questions")
    options = relationship("Options", back_populates="question", cascade="all, delete-orphan")
    answers = relationship("Answers", back_populates="question", cascade="all, delete-orphan")
    source_logics = relationship("Logic", foreign_keys="[Logic.source_question_id]", back_populates="source_question")
    target_logics = relationship("Logic", foreign_keys="[Logic.target_question_id]", back_populates="target_question")
    responses = relationship("Response", back_populates="question", cascade="all, delete-orphan")
