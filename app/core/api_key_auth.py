from datetime import datetime
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models.api_key import ApiKey
from app.core.redis_client import redis_client


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)


def get_user_from_api_key(api_key: str = Security(api_key_header)):
    db: Session = SessionLocal()

    # 🔍 get key
    key = db.query(ApiKey).filter(ApiKey.key == api_key).first()

    if not key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 🔥 PLAN LIMITS
    plan_limits = {
        "free": 10,
        "pro": 100,
        "enterprise": 1000
    }

    rate_limit = plan_limits.get(key.plan, 10)

    # 🔥 REDIS RATE LIMIT
    window = 60
    redis_key = f"rate_limit:{api_key}"

    requests = redis_client.incr(redis_key)

    if requests == 1:
        redis_client.expire(redis_key, window)

    if requests > rate_limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # 🔥 TRACK USAGE
    key.requests_count += 1
    key.last_request_at = datetime.utcnow()

    db.commit()

    return {
        "user_id": key.user_id,
        "plan": key.plan        
    }

