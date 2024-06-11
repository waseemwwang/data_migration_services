from fastapi import APIRouter

user_router = APIRouter()


@user_router.get("/users/")
async def read_users():
    return [{"username": "user1"}, {"username": "user2"}]


@user_router.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"username": f"user{user_id}"}
