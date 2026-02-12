from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.project import Project
from app.db.models.project_member import ProjectMember
from app.db.models.user import User
from app.core.security import get_current_user
from app.utils.enums import ProjectRole
from app.db.models.audit_log import AuditLog


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
def create_project(
    name: str,
    description: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create project
    project = Project(name=name, description=description)
    db.add(project)
    db.commit()
    db.refresh(project)

    

    # Assign OWNER role to creator
    membership = ProjectMember(
        user_id=current_user.id,
        project_id=project.id,
        role=ProjectRole.OWNER.value
    )

    db.add(membership)
    db.commit()

    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE_PROJECT",
        target_type="PROJECT",
        target_id=project.id
    )
    db.add(audit)
    db.commit()

    return {
        "project_id": project.id,
        "name": project.name,
        "owner": current_user.email
    }


@router.get("/")
def list_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    memberships = db.query(ProjectMember).filter(
        ProjectMember.user_id == current_user.id
    ).all()

    result = []
    for m in memberships:
        if not m.project.is_deleted:
            result.append({
                "project_id": m.project.id,
                "name": m.project.name,
                "role": m.role
            })

    return result


@router.post("/{project_id}/members")
def add_project_member(
    project_id: int,
    user_email: str,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ Check project exists
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2️⃣ Check current user membership
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    # 3️⃣ Only OWNER can add members
    if membership.role != ProjectRole.OWNER.value:
        raise HTTPException(status_code=403, detail="Only OWNER can add members")

    # 4️⃣ Validate role assignment (strict RBAC)
    allowed_roles = [
        ProjectRole.ADMIN.value,
        ProjectRole.MEMBER.value
    ]

    if role not in allowed_roles:
        raise HTTPException(status_code=400, detail="Invalid role assignment")

    # 5️⃣ Find user to add
    user_to_add = db.query(User).filter(
        User.email == user_email
    ).first()

    if not user_to_add:
        raise HTTPException(status_code=404, detail="User not found")

    # 6️⃣ Prevent duplicate membership
    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == user_to_add.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already a member")

    # 7️⃣ Add membership
    new_membership = ProjectMember(
        user_id=user_to_add.id,
        project_id=project_id,
        role=role
    )

    db.add(new_membership)
    db.commit()

    return {
        "message": "Member added successfully",
        "project_id": project_id,
        "user": user_email,
        "role": role
    }


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ Check project exists
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2️⃣ Check membership
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    # 3️⃣ Only OWNER can delete
    if not has_permission("add_member",membership.role):
        raise HTTPException(status_code=403, detail="Only OWNER can delete project")

    # 4️⃣ Soft delete
    project.is_deleted = True
    db.commit()

    return {"message": "Project deleted successfully"}
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ Check project exists and not deleted
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2️⃣ Check membership
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(status_code=403, detail="Not a project member")

    # 3️⃣ Only OWNER can delete
    if membership.role != ProjectRole.OWNER.value:
        raise HTTPException(status_code=403, detail="Only OWNER can delete project")

    # 4️⃣ Soft delete
    project.is_deleted = True
    db.commit()

    return {"message": "Project deleted successfully"}
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ Check project exists and not deleted
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2️⃣ Check membership
    existing_membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not existing_membership:
        membership =ProjectMember(
            user_id=current_user.id,
            project_id=project_id,
            role=ProjectRole.MEMBER.value
        )
        db.add(membership)
        db.commit()

    # 3️⃣ Only OWNER can delete
    if membership.role != ProjectRole.OWNER.value:
        raise HTTPException(status_code=403, detail="Only OWNER can delete project")

    # 4️⃣ Soft delete
    project.is_deleted = True
    db.commit()

    return {"message": "Project deleted successfully"}



@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ Check project exists and not deleted
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2️⃣ Check membership
    membership = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == current_user.id
    ).first()

    if not membership:
        raise HTTPException(status_code=404, detail="Project not found")

    # 3️⃣ Only OWNER can delete
    if membership.role != ProjectRole.OWNER.value:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 4️⃣ Soft delete
    project.is_deleted = True
    db.commit()

    return {"message": "Project deleted successfully"}


    audit = AuditLog(
        user_id=current_user.id,
        action="CREATE_PROJECT",
        target_type="PROJECT",
        target_id=project.id
    )   
    db.add(audit)
    db.commit()  