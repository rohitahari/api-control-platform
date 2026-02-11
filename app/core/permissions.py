from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models.project_member import ProjectMember
from app.db.models.task import Task
from app.utils.enums import ProjectRole


permission_map = {
    "delete_task": [ProjectRole.OWNER.value, ProjectRole.ADMIN.value],
    "create_task": [ProjectRole.OWNER.value, ProjectRole.ADMIN.value, ProjectRole.MEMBER.value],
    "add_member": [ProjectRole.OWNER.value],
    "delete_project": [ProjectRole.OWNER.value],
    "update_task": [ProjectRole.OWNER.value, ProjectRole.ADMIN.value, ProjectRole.MEMBER.value],
}


def get_membership(project_id: int, user_id: int, db: Session):
    return db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_id
    ).first()


def require_project_permission(
    project_id: int,
    user_id: int,
    action: str,
    db: Session,
    resource_id: int | None = None
):
    membership = get_membership(project_id, user_id, db)

    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    allowed_roles = permission_map.get(action)

    if allowed_roles and membership.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Permission denied")

    # ABAC condition for update_task
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

    return membership





# TOD:integrate audit loggin here


# test  change 1



# cycle 3 test change


