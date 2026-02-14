from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.user import User
from app.db.models.project import Project
from app.core.security import get_current_user
from app.services import project_service
from app.core.permissions import enforce_policy

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/")
def create_project(
    name: str,
    description: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.create_project(
        name=name,
        description=description,
        user_id=current_user.id,
        db=db
    )


@router.get("/{project_id}")
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enforce_policy(
        action="update_project",   # membership check only
        project_id=project_id,
        user_id=current_user.id,
        db=db
    )

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "project_id": project.id,
        "name": project.name,
        "description": project.description
    }


@router.patch("/{project_id}")
def update_project(
    project_id: int,
    name: str | None = None,
    description: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    enforce_policy(
        action="update_project",
        project_id=project_id,
        user_id=current_user.id,
        db=db
    )

    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_deleted == False
    ).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

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



@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.delete_project(
        project_id=project_id,
        user_id=current_user.id,
        db=db
    )



# discipline 1: project management
# discipline 2: HR management  

