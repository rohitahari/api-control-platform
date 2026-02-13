from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.permissions import enforce_policy
from app.services import task_service

from app.db.session import get_db
from app.db.models.task import Task
from app.db.models.project import Project
from app.db.models.project_member import ProjectMember
from app.db.models.user import User
from app.core.security import get_current_user
from app.utils.enums import ProjectRole, TaskStatus, TaskPriority




router = APIRouter(prefix="/projects", tags=["Tasks"])


def get_membership(project_id: int, user_id: int, db: Session):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()

@router.post("/{project_id}/tasks")
def create_task(
    project_id: int,
    title: str,
    description: str | None = None,
    priority: str = TaskPriority.MEDIUM.value,
    due_date: datetime | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = task_service.create_task(
        project_id=project_id,
        user_id=current_user.id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        db=db
    )

    

    return {
        "task_id": task.id,
        "title": task.title,
        "priority": task.priority,
        "created_by": current_user.email
    }




from typing import Optional

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
    

    query = db.query(Task).filter(
        Task.project_id == project_id
    ).order_by(Task.id.asc())

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



@router.put("/{project_id}/tasks/{task_id}")
def delete_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enforce_policy(
        action="delete_task",
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

    db.delete(task)
    db.commit()

    return {"detail": "Task deleted"}

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
    enforce_policy(
        action="delete_task",
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

    db.delete(task)
    db.commit()

    return {"detail": "Task deleted"}

# test commit 2


# cycle 2 test change



