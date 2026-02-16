from pydantic import BaseModel
from typing import Optional
from app.schema.project import ProjectResponse, ProjectCreate, ProjectUpdate


class ProjectResponse(BaseModel):
    project_id: int
    name: str
    description: Optional[str] = None



    class Config:
        from_attributes = True