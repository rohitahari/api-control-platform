from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------
# CREATE
# -----------------------
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


# -----------------------
# UPDATE
# -----------------------
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# -----------------------
# RESPONSE
# -----------------------
class ProjectResponse(BaseModel):
    project_id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
