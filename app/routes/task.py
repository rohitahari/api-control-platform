from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.core.security import get_current_user
from app.services import task_service

router = APIRouter(prefix="/projects", tags=["Tasks"])


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
    task_service.delete_task(
        project_id=project_id,
        task_id=task_id,
        user_id=current_user.id,
        db=db
    )

    return {"detail": "Task deleted"}
