from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from apps.project import project_router
from apps.user import user_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含用户路由
app.include_router(user_router, prefix="/users", tags=["users"])

# 包含项目路由
app.include_router(project_router, prefix="/projects", tags=["projects"])
