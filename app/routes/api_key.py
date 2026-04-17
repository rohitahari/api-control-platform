from app.db.models import api_key
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.core.api_key_auth import get_user_from_api_key
from app.services.api_key_service import generate_api_key
from app.db.models.user import User
from app.db.models.api_key import ApiKey

# ✅ THIS MUST EXIST
router = APIRouter(tags=["API Keys"])


# 🔑 CREATE API KEY (JWT protected)
@router.post("/")
def create_api_key(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return generate_api_key(
        user_id=current_user.id,
        db=db
    )


# 🔐 TEST API KEY (X-API-Key header)
@router.get("/test-api-key")
def api_key_test(current_key=Security(get_user_from_api_key)):
    return {
        "message": "API key works",
        "user_id": current_key["user_id"]
    }



@router.get("/usage")
def get_usage(
    current_key=Security(get_user_from_api_key),
    db: Session = Depends(get_db)
):
    if not current_key:
        return {"error": "API key not found"}

    key = db.query(ApiKey).filter(ApiKey.user_id == current_key["user_id"]).first()

    return {
        "key": key.key,
        "last_used_at": key.last_request_at,
        "usage_count": key.requests_count
    }

