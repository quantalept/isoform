from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class FormsModel(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True)
    admin_user_id = Column(UUID(as_uuid=True), ForeignKey("admin_user.admin_user_id"))
    # other fields...

    admin_user = relationship("AdminUserModel", back_populates="forms")
