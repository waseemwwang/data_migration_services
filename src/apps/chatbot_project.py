from fastapi import APIRouter

project_router = APIRouter()


@project_router.get("/", response_model="dict")
async def read_projects():
    return [{"project_name": "project1"}, {"project_name": "project2"}]


@project_router.get("/{project_id}", response_model="dict")
async def read_project(project_id: int):
    return {"project_name": f"project{project_id}"}
