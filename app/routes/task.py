from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.permissions import enforce_policy
from app.db.base_class import Base
from app.db.session import get_db
from app.db.models.user import User
from app.core.security import get_current_user
from app.services import task_service
from sqlalchemy import Column,Boolean, ForeignKey, Integer, String, Text

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/{project_id}/tasks")
def create_task(
    project_id: int,
    title: str,
    description: str | None = None,
    priority: str = "MEDIUM",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_service.create_task(
        project_id=project_id,
        title=title,
        description=description,
        priority=priority,
        user_id=current_user.id,
        db=db
    )


@router.patch("/{project_id}/tasks/{task_id}")
def update_task(
    project_id: int,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_service.update_task(
        project_id=project_id,
        task_id=task_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        user_id=current_user.id,
        db=db
    )


@router.delete("/{project_id}/tasks/{task_id}")
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_service.delete_task(
        project_id=project_id,
        task_id=task_id,
        user_id=current_user.id,
        db=db
    )

    return {"detail": "Task deleted"}



@router.post("/{project_id}/tasks/{task_id}/archive")
def archive_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_service.archive_task(
        project_id=project_id,
        task_id=task_id,
        user_id=current_user.id,
        db=db
    )

@router.get("/{project_id}/tasks/summary")
def task_summary(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enforce_policy(
        action="update_project",  # membership check only
        project_id=project_id,
        user_id=current_user.id,
        db=db
    )

    return task_service.get_project_task_summary(
        project_id=project_id,
        db=db
    )



# ABAC 

# Git discipline2  