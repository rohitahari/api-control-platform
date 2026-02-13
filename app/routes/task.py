from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db.session import get_db
from app.db.models.task import Task
from app.db.models.project import Project
from app.db.models.user import User
from app.core.security import get_current_user
from app.utils.enums import TaskStatus, TaskPriority
from app.core.permissions import enforce_policy


router = APIRouter(prefix="/projects", tags=["Tasks"])

# RBAC + ABAC Enforcement in Task Routes

@router.post("/{project_id}/tasks")
def create_task(
    project_id: int,
    title: str,
    description: Optional[str] = None,
    priority: str = TaskPriority.MEDIUM.value,
    due_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1️⃣ Check project exists
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2️⃣ Enforce permission
    enforce_policy(
        action="create_task",
        project_id=project_id,
        user_id=current_user.id,
        db=db
    )

    # 3️⃣ Validate priority
    if priority not in [p.value for p in TaskPriority]:
        raise HTTPException(status_code=400, detail="Invalid priority")

    # 4️⃣ Create task
    task = Task(
        project_id=project_id,
        created_by=current_user.id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "task_id": task.id,
        "title": task.title,
        "priority": task.priority
    }



@router.get("/{project_id}/tasks")
def list_tasks(
    project_id: int,
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1️⃣ Must be project member to list
    enforce_policy(
        action="create_task",  # any valid membership action works for membership validation
        project_id=project_id,
        user_id=current_user.id,
        db=db
    )

    query = db.query(Task).filter(
        Task.project_id == project_id
    )

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    tasks = query.offset(skip).limit(limit).all()

    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "due_date": t.due_date
        }
        for t in tasks
    ]



#cds

@router.patch("/{project_id}/tasks/{task_id}")
def update_task(
    project_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1️⃣ Centralized RBAC + ABAC
    enforce_policy(
        action="update_task",
        project_id=project_id,
        user_id=current_user.id,
        db=db,
        resource_id=task_id
    )

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.project_id == project_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 2️⃣ Validate enums
    if status and status not in [s.value for s in TaskStatus]:
        raise HTTPException(status_code=400, detail="Invalid status")

    if priority and priority not in [p.value for p in TaskPriority]:
        raise HTTPException(status_code=400, detail="Invalid priority")

    # 3️⃣ Apply updates
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

    return {
        "task_id": task.id,
        "title": task.title,
        "status": task.status,
        "priority": task.priority
    }



@router.delete("/{project_id}/tasks/{task_id}")
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1️⃣ Enforce RBAC
    enforce_policy(
        action="delete_task",
        project_id=project_id,
        user_id=current_user.id,
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

    return {"detail": "Task deleted"}
