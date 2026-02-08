from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.audit_log import AuditLog
from app.core.security import get_current_user
router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/logs")
def get_audit_logs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    logs = db.query(AuditLog).filter(AuditLog.user_id == current_user.id).all()
    return logs

