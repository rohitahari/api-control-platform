from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.project import Project
from app.db.models.project_member import ProjectMember
from app.db.models.user import User
from app.db.models.audit_log import AuditLog
from app.db.session import get_db
from app.utils.enums import ProjectRole
from app.core.permissions import enforce_policy


def get_project(project_id: int, user_id: int, db: Session):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    enforce_policy(
        action="view_project",
        project_id=project_id,
        user_id=user_id,
        db=db
    )

    return {
        "project_id": project.id,
        "name": project.name,
        "description": project.description
    }


def delete_project(project_id: int, user_id: int, db: Session):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    enforce_policy(
        action="delete_project",
        project_id=project_id,
        user_id=user_id,
        db=db
    )

    project.is_deleted = True
    db.commit()

    return {"message": "Project deleted successfully"}







def update_project(
    project_id: int,
    name: str | None,
    description: str | None,
    user_id: int,
    db: Session
):
    # 1️⃣ Permission check
    enforce_policy(
        action="update_project",
        project_id=project_id,
        user_id=user_id,
        db=db
    )

    # 2️⃣ Fetch project
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 3️⃣ Update fields
    if name:
        project.name = name

    if description:
        project.description = description

    db.commit()
    db.refresh(project)

    return {
        "project_id": project.id,
        "name": project.name,
        "description": project.description
    }


        