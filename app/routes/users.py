from fastapi import APIRouter, Depends
from app.db.models.user import User
from app.core.security import get_current_user


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.system_role,
    }