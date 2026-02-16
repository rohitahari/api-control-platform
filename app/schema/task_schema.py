from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# -----------------------
# CREATE
# -----------------------
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "MEDIUM"
    due_date: Optional[datetime] = None


# -----------------------
# UPDATE
# -----------------------
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


# -----------------------
# RESPONSE
# -----------------------
class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    due_date: Optional[datetime]

    class Config:
        from_attributes = True
