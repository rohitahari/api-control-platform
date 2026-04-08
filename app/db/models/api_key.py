from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.db.base_class import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)

    # ✅ TRACKING FIELDS (THIS WAS MISSING)
    requests_count = Column(Integer, default=0)
    last_request_at = Column(DateTime, nullable=True)
    plan = Column(String, default="free")  # free, pro, enterprise  


    