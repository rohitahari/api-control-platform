from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.task import Task
from app.db.models.project import Project
from app.utils.enums import TaskPriority


def create_task(
    project_id: int,
    user_id: int,
    title: str,
    description: str | None,
    priority: str,
    due_date,
    db: Session
):
    # 1️⃣ Ensure project exists
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

   

    # 3️⃣ Validate priority
    if priority not in [p.value for p in TaskPriority]:
        raise HTTPException(status_code=400, detail="Invalid priority")

    # 4️⃣ Create task
    task = Task(
        project_id=project_id,
        created_by=user_id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

