from fastapi import APIRouter

project_router = APIRouter()

@project_router.get("/projects/")
async def read_projects():
    return [{"project_name": "project1"}, {"project_name": "project2"}]

@project_router.get("/projects/{project_id}")
async def read_project(project_id: int):
    return {"project_name": f"project{project_id}"}