from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base



class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    status = Column(String, default="TODO", nullable=False)
    priority = Column(String, default="MEDIUM", nullable=False)

    due_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="tasks")
    creator = relationship("User")
