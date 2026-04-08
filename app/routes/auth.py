 
from app.schemas.response import ApiResponse
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.enums import SystemRole
from app.utils.response import success_response



from pydantic import BaseModel, Field



from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.api_key import ApiKey

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_user_from_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    db: Session = SessionLocal()

    key = db.query(ApiKey).filter(ApiKey.key == api_key).first()

    if not key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return key.user_id







class RegisterRequest(BaseModel):
    email: str
    password: str = Field(..., max_length=72)


router = APIRouter(tags=["Authentication"])


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(request.password)

    new_user = User(
        email=request.email,
        hashed_password=hashed_pw,
        system_role=SystemRole.USER.value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"sub": str(new_user.id)})

    return success_response(
    data={
        "access_token": access_token,
        "token_type": "bearer"
    }
)










@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
