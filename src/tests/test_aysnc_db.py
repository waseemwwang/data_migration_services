import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.database import SessionManager, Base, async_session_factories
from models.chatbot_auth import ChatbotUser
from tests.crud import get_user_by_id
from utils.logger import log


# @pytest.fixture(scope="module")
# async def setup_database():
#     engine = async_engines["base"]
#     async with engine.begin() as conn:
#         # 清除并重建数据库
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

#     session = async_session_factories["base"]
#     async with session() as session:
#         # 添加测试数据
#         user = ChatbotUser(name="testuser", email="testuser@example.com")
#         session.add(user)
#         print(user)
#         log.info(f"session: {session}")
#         await session.commit()

#     yield
#     # 清理数据库
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture
# async def db_session():
#     async with async_session_factories["base"]() as session:
#         yield session


@pytest.mark.asyncio
async def test_get_user_by_id():
    async with SessionManager("base") as session:
        user = ChatbotUser(name="testuser", email="testuser@example.com", alias="xxx", role="admin")
        log.info(f"user: {user}")
        log.info(f"session: {dir(session)}")
        session.add(user)
        await session.commit()

        user_id = 1
        user = await get_user_by_id(session, user_id)
        log.debug(user)
        assert user is not None
        assert user.id == user_id
        assert user.name == "testuser"
        assert user.email == "testuser@example.com"
