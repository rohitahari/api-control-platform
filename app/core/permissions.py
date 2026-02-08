from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.project_member import ProjectMember
from app.utils.enums import ProjectRole


def get_membership(project_id: int, user_id: int, db: Session):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()


def require_project_permission(
    project_id: int,
    user_id: int,
    action: str,
    db
):
    membership = get_membership(project_id, user_id, db)

    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    permission_map = {
        "delete_task": [ProjectRole.OWNER.value, ProjectRole.ADMIN.value],
        "create_task": [ProjectRole.OWNER.value, ProjectRole.ADMIN.value, ProjectRole.MEMBER.value],
        "add_member": [ProjectRole.OWNER.value],
        "delete_project": [ProjectRole.OWNER.value],
    }

    allowed_roles = permission_map.get(action)

    if allowed_roles and membership.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Permission denied")

    return membership



# RBAC permission mapping centralized in one place
# pagination and filtering logic can also be added here in the future