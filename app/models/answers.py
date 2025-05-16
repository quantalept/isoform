from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
from app.db.base import Base

class Answers(Base):
    __tablename__ = "answers"

    answer_id = Column(UUID, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("responses.response_id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)
    answer_text = Column(JSONB, nullable=False)  # 👈 JSONB instead of String

    # Relationships
    response = relationship("Response", back_populates="answers")
    question = relationship("Questions", back_populates="answers")