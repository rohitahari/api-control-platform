from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    role = Column(String, default="member")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ RELATIONSHIPS (THIS WAS MISSING)
    user = relationship("User", back_populates="project_members")
    project = relationship("Project", back_populates="members")

    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="unique_project_user"),
    )