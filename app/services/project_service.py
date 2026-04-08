from sqlalchemy.orm import Session

from app.db.models.project import Project
from app.db.models.project_member import ProjectMember
from app.db.models.user import User
from app.db.models.audit_log import AuditLog

from app.core.permissions import enforce_policy
from app.core.exceptions import AppException


# ✅ CREATE PROJECT
def create_project(name: str, description: str, user_id: int, db: Session):
    project = Project(
        name=name,
        description=description,
        is_deleted=False
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    # Add creator as OWNER
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
        raise AppException("Project not found", 404)

    enforce_policy(
        action="view_project",
        project_id=project_id,
        user_id=user_id,
        db=db
    )

    return project


# ✅ UPDATE PROJECT
def update_project(project_id: int, name, description, user_id: int, db: Session):

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise AppException("Project not found", 404)

    enforce_policy(
        action="update_project",
        project_id=project_id,
        user_id=user_id,
        db=db
    )

    if name:
        project.name = name

    if description:
        project.description = description

    db.commit()
    db.refresh(project)

    return project


# ✅ DELETE PROJECT
def delete_project(project_id: int, user_id: int, db: Session):

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise AppException("Project not found", 404)

    project.is_deleted = True

    log = AuditLog(
        project_id=project.id,
        user_id=user_id,
        action="delete_project"
    )

    db.add(log)
    db.commit()

    return {"message": "Project deleted"}


# ✅ ADD MEMBER (IMPORTANT FEATURE)
def add_member(project_id: int, email: str, inviter_id: int, db: Session):

    enforce_policy(
        action="invite_member",
        project_id=project_id,
        user_id=inviter_id,
        db=db
    )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise AppException("User not found", 404)

    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user.id
    ).first()

    if existing:
        raise AppException("User already a member", 400)

    member = ProjectMember(
        project_id=project_id,
        user_id=user.id,
        role="member"
    )

    db.add(member)
    db.commit()

    return {"message": "User added to project"}