from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

from app.utils.enums import SystemRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    system_role = Column(String, default=SystemRole.USER.value, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    memberships = relationship(
        "ProjectMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )


    project_members = relationship("ProjectMember", back_populates="user")

