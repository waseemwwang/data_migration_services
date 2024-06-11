import traceback
from typing import Union

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from apps.project import project_router
from apps.user import user_router
from logger import log


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    log.info(f"Request: {request.method} {request.url}")

    response = await call_next(request)

    log.info(f"Response status: {response.status_code}")

    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    log.error(f"HTTP exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 使用 traceback 记录详细的异常堆栈信息
    exc_info = traceback.format_exc()
    log.error(f"Unhandled exception: {exc_info}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )


# 包含用户路由
app.include_router(user_router, prefix="/users", tags=["users"])

# 包含项目路由
app.include_router(project_router, prefix="/projects", tags=["projects"])
