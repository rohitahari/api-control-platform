from sqlalchemy.orm import Session
from fastapi import HTTPException


from app.db.models.project import Project
from app.db.models.project_member import ProjectMember
from app.core.permissions import enforce_policy
from app.core.exceptions import AppException

from app.db.models.audit_log import AuditLog





# ✅ CREATE PROJECT
def create_project(name: str, description: str, user_id: int, db: Session):


    # 1️⃣ Create project
    project = Project(
        name=name,
        description=description,
        is_deleted=False
    )


    db.add(project)
    db.commit()
    db.refresh(project)


    # 2️⃣ Add creator as OWNER
    membership = ProjectMember(
        project_id=project.id,
        user_id=user_id,
        role="owner"
    )


    db.add(membership)
    db.commit()


    return project




# ✅ GET PROJECT
def get_project(project_id: int, user_id: int, db: Session):


    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()


    if not project:
        raise AppException(
            status_code=404,
            error="PROJECT_NOT_FOUND",
            message="Project not found"
        )


    # Permission check (membership + RBAC/ABAC)
    enforce_policy(
        action="view_project",
        project_id=project_id,
        user_id=user_id,
        db=db
    )


    return project




# ✅ UPDATE PROJECT
def update_project(
    project_id: int,
    name: str | None,
    description: str | None,
    user_id: int,
    db: Session
):


    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()


    if not project:
        raise AppException(
            status_code=404,
            error="PROJECT_NOT_FOUND",
            message="Project not found"
        )


    enforce_policy(
        action="update_project",
        project_id=project_id,
        user_id=user_id,
        db=db
    )


    if name is not None:
        project.name = name


    if description is not None:
        project.description = description


    db.commit()
    db.refresh(project)


    return project




# ✅ DELETE PROJECT (SOFT DELETE)
from app.db.models.audit_log import AuditLog
from app.core.exceptions import AppException
from app.db.models.project import Project
from sqlalchemy.orm import Session


def delete_project(project_id: int, user_id: int, db: Session):

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise AppException(
            status_code=404,
            error="PROJECT_NOT_FOUND",
            message="Project not found"
        )

    # soft delete
    project.is_deleted = True

    # audit log
    log = AuditLog(
        project_id=project.id,
        user_id=user_id,
        action="delete_project"
    )

    db.add(log)
    db.commit()

    return {"message": "Project deleted successfully"}

