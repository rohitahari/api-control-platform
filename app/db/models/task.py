from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from sqlalchemy import Boolean
from sqlalchemy.sql import func



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

    is_archived = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    archived_at = Column(DateTime(timezone=True), nullable=True)


    project = relationship("Project", back_populates="tasks")
    creator = relationship("User")



class TaskComment(Base):
    __tablename = "task_comments"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer,ForeignKey("projects.id"),nullable=False)

    task_id = Column(Integer,ForeignKey("tasks.id:"),nullable= False)
    created_by = Column(Integer,ForeignKey("users.id"), nullable=False)

    content = Column(String, nullable =False)


    is_deleted = Column(Boolean, default=False, nullable=False)

    created_by = Column(DateTime(timezone=True),service_default=func.now())
    updated_at = Column(DateTime(timezone =True),onupdate=func.now())


    

    