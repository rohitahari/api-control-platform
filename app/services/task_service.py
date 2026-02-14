from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from app.db.models.task import Task
from app.core.permissions import enforce_policy


def create_task(
    project_id: int,
    title: str,
    description: str | None,
    priority: str,
    user_id: int,
    db: Session
):
    enforce_policy(
        action="create_task",
        project_id=project_id,
        user_id=user_id,
        db=db
    )

    task = Task(
        title=title,
        description=description,
        priority=priority,
        project_id=project_id,
        created_by=user_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(
    project_id: int,
    task_id: int,
    title: str | None,
    description: str | None,
    status: str | None,
    priority: str | None,
    user_id: int,
    db: Session
):
    enforce_policy(
        action="update_task",
        project_id=project_id,
        user_id=user_id,
        db=db,
        resource_id=task_id
    )

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.project_id == project_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if title:
        task.title = title
    if description:
        task.description = description
    if status:
        task.status = status
    if priority:
        task.priority = priority

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    project_id: int,
    task_id: int,
    user_id: int,
    db: Session
):
    enforce_policy(
        action="delete_task",
        project_id=project_id,
        user_id=user_id,
        db=db
    )

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.project_id == project_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
