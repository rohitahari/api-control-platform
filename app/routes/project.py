from app.core.api_key_auth import get_user_from_api_key
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.core.security import get_current_user

from app.services import project_service
from app.schema.project_schema import ProjectCreate, ProjectResponse
from app.utils.response import success_response

router = APIRouter(prefix="/projects", tags=["Projects"])


# ✅ CREATE PROJECT
@router.post("/", response_model=ProjectResponse)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = project_service.create_project(
        name=payload.name,
        description=payload.description,
        user_id=current_user.id,
        db=db
    )

    return project


# ✅ GET PROJECT
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.get_project(
        project_id=project_id,
        user_id=current_user.id,
        db=db
    )


# ✅ UPDATE PROJECT
@router.patch("/{project_id}")
def update_project(
    project_id: int,
    name: str = None,
    description: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.update_project(
        project_id=project_id,
        name=name,
        description=description,
        user_id=current_user.id,
        db=db
    )


# ✅ DELETE PROJECT
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


# ✅ INVITE USER (NEW FEATURE)
@router.post("/{project_id}/invite")
def invite_user(
    project_id: int,
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return project_service.add_member(
        project_id=project_id,
        email=email,
        inviter_id=current_user.id,
        db=db
    )



@router.get("/api-key-test")
def api_key_test(user_id: int = Depends(get_user_from_api_key)):
    return {"message": "API key working", "user_id": user_id}