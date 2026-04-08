import secrets
from sqlalchemy.orm import Session

from app.db.models.api_key import ApiKey


def generate_api_key(user_id: int, db: Session, name:str | None = None):
    key = secrets.token_hex(32)

    api_key = ApiKey(
        key=key,
        user_id=user_id,
        name=name
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return {
        "key": api_key.key
    }
