from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy import Enum as SqlEnum
from enum import Enum
from app.utils.enums import OptionType

class Options(Base):
    __tablename__ = "options"

    option_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)
    option_text = Column(String, nullable=False)
    option_type = Column(SqlEnum(OptionType), nullable=False)
    order = Column(Integer, nullable=False)

    # Optional relationships (if you want to easily access related data)
    question = relationship("Questions", back_populates="options")