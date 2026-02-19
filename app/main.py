from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.project import router as project_router
from app.routes.task import router as task_router
from app.routes.audit import router as audit_router
from app.routes.users import router as users_router
from app.Infrastructure.scheduler import start_scheduler

from app.core.config import settings



from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.schema.error_schema import ErrorResponse, ErrorDetail


if settings.ENV =="prod":
    app = FastAPI(docs_url=None,redoc_url = None)
else:
    app =FastAPI()

app = FastAPI()   # ← MUST be defined BEFORE include_router



app.include_router(auth_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(audit_router)
app.include_router(users_router)


@app.get("/")
def health_check():
    return {"status": "Backend is running"}


@app.on_event("startup")
def startup_event():
    start_scheduler()




from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException


@app.exception_handler(AppException)
async def custom_app_exception_handler(request: Request, exc: AppException):

    # If detail is already structured dict
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.detail.get("error"),
                    "message": exc.detail.get("message"),
                    "status": exc.status_code
                }
            }
        )

    # If detail is plain string
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": str(exc.detail).replace(" ", "_").upper(),
                "message": exc.detail,
                "status": exc.status_code
            }
        }
    )
