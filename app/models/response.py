from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime 
from app.db.base import Base

class Response(Base):
    __tablename__ = "responses"

    response_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=True)
    form_id = Column(UUID(as_uuid=True), ForeignKey("forms.form_id"), nullable=False)
    submited_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)
    answer_text = Column(String, nullable=False)  # Assuming answer_text is a string

    # Relationships
    form = relationship("FormsModel", back_populates="responses")
    answers = relationship("Answers", back_populates="response", cascade="all, delete-orphan")
    question = relationship("Questions", back_populates="responses")