from sqlalchemy import func
from app.db.models.task import Task


def get_project_task_summary(project_id: int, db):
    total = db.query(func.count(Task.id)).filter(
        Task.project_id == project_id
    ).scalar()

    completed = db.query(func.count(Task.id)).filter(
        Task.project_id == project_id,
        Task.status == "DONE",
        Task.is_archived == False
    ).scalar()

    pending = db.query(func.count(Task.id)).filter(
        Task.project_id == project_id,
        Task.status != "DONE",
        Task.is_archived == False
    ).scalar()

    archived = db.query(func.count(Task.id)).filter(
        Task.project_id == project_id,
        Task.is_archived == True
    ).scalar()

    completion_rate = 0
    if total and total > 0:
        completion_rate = round((completed / total) * 100, 2)

    return {
        "total_tasks": total,
        "completed": completed,
        "pending": pending,
        "archived": archived,
        "completion_rate_percent": completion_rate
    }
