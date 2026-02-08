from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base

from app.utils.enums import ProjectRole

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)




    role = Column(String, default=ProjectRole.MEMBER.value, nullable=False)


    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="unique_user_project"),
    )

    # Relationships
    user = relationship("User", back_populates="memberships")
    project = relationship("Project", back_populates="members")
