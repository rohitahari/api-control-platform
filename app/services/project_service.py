from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.project import Project
from app.db.models.project_member import ProjectMember
from app.db.models.user import User
from app.db.models.audit_log import AuditLog
from app.utils.enums import ProjectRole
from app.core.permissions import enforce_policy


def create_project(name: str, description: str | None, user_id: int, db: Session):
    project = Project(name=name, description=description)
    db.add(project)
    db.flush()

    membership = ProjectMember(
        user_id=user_id,
        project_id=project.id,
        role=ProjectRole.OWNER.value
    )
    db.add(membership)

    audit = AuditLog(
        user_id=user_id,
        action="CREATE_PROJECT",
        target_type="PROJECT",
        target_id=project.id
    )
    db.add(audit)

    db.commit()
    db.refresh(project)

    return {
        "project_id": project.id,
        "name": project.name
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
