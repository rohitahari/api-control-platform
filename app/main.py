from fastapi import FastAPI
from app.routes.api_key import router as api_key_router

from app.routes.auth import router as auth_router
from app.routes.project import router as project_router
from app.routes.task import router as task_router
from app.routes.audit import router as audit_router
from app.routes.users import router as users_router

from app.core.config import settings



from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.schema.error_schema import ErrorResponse, ErrorDetail


app = FastAPI(
    title="SAAS Backend API",
    docs_url=None if settings.ENV == "prod" else "/docs",
    redoc_url=None if settings.ENV == "prod" else "/redoc"
)   # ← MUST be defined BEFORE include_router




from app.routes.api_key import router as api_key_router








from app.core.exceptions import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    AppException
)

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


if settings.ENV =="prod":
    app = FastAPI(docs_url=None,redoc_url = None)
else:
    app =FastAPI()




app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(project_router, prefix="/api/v1/projects")
app.include_router(task_router, prefix="/api/v1/tasks")
app.include_router(api_key_router, prefix="/api/v1/api-keys", tags=["API Keys"])



@app.get("/")
def health_check():
    return {"status": "Backend is running"}


@app.on_event("startup")
def startup_event():
    print("Starting up the SAAS Backend API...")
   



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




from fastapi.responses import JSONResponse
from fastapi import Request


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
            "data": None
        },
    )


docs_url="/docs"
