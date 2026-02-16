from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.project_member import ProjectMember
from app.db.models.task import Task
from app.utils.enums import ProjectRole


permission_map = {
    "delete_task":["OWNER", "ADMIN"],
    "update_task":["OWNER", "ADMIN", "MEMBER"],
    "create_task":["OWNER", "ADMIN", "MEMBER"],
    "delete_project":["OWNER"],
    "add_member":["OWNER"],
    "update_project":["OWNER", "ADMIN"],
    "view_archived_tasks":["OWNER", "ADMIN"],
    "restore_task":["OWNER", "ADMIN"],
    "archive_task":["OWNER", "ADMIN", "MEMBER"]
}



# Membership Lookup

def get_membership(project_id: int, user_id: int, db: Session):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()




# Role Validation (RBAC)

def validate_role(action: str, membership):
    allowed_roles = permission_map.get(action)

    if not allowed_roles:
        raise HTTPException(status_code=400, detail="Invalid action")

   




# Attribute Validation (ABAC Layer)

def validate_attributes(
    action: str,
    membership,
    project_id: int,
    user_id: int,
    db: Session,
    resource_id: int | None
):
    # MEMBER can only update their own tasks
    if action == "update_task" and membership.role == ProjectRole.MEMBER.value:

        task = db.query(Task).filter(
            Task.id == resource_id,
            Task.project_id == project_id
        ).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if task.created_by != user_id:
            raise HTTPException(
                status_code=403,
                detail="Members can only update their own tasks"
            )


def enforce_policy(
    action: str,
    project_id: int,
    user_id: int,
    db: Session,
    resource_id: int | None = None
):
    # 1️⃣ Membership check
    membership = get_membership(project_id, user_id, db)

    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    # 2️⃣ RBAC
    validate_role(action, membership)

    # 3️⃣ ABAC
    validate_attributes(
        action,
        membership,
        project_id,
        user_id,
        db,
        resource_id
    )

    return membership
