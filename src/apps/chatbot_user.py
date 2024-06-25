from fastapi import APIRouter
from utils.response import make_response

user_router = APIRouter()


@user_router.get("/", response_model="dict")
async def read_users():
    return make_response()


@user_router.get("/{user_id}", response_model="dict")
async def read_user(user_id: int):
    return make_response()


@user_router.post("/", response_model="dict")
async def create_user():
    return make_response()


@user_router.put("/{user_id}", response_model="dict")
async def create_user(user_id: int):
    return make_response()


@user_router.delete("/{user_id}", response_model="dict")
async def create_user(user_id: int):
    return make_response()


@user_router.post("/", response_model="dict")
async def create_user(user_id: int):
    return make_response()
