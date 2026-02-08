from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.project import router as project_router
from app.routes.task import router as task_router
from app.routes.audit import router as audit_router
from app.routes.users import router as users_router


app = FastAPI()   # ← MUST be defined BEFORE include_router



app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(audit_router)
app.include_router(users_router)


@app.get("/")
def health_check():
    return {"status": "Backend is running"}
