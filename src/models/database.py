import contextlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import GlobalConfig
from sqlalchemy.pool import QueuePool
from utils.logger import log
from contextlib import contextmanager


# 创建连接池和会话工厂
engines = {}
session_factories = {}

async_engines = {}
async_session_factories = {}
for db_name, config in GlobalConfig.get_database_mysql().items():
    db_url = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset={config['charset']}"
    engine = create_engine(
        db_url,
        poolclass=QueuePool,
        pool_size=config["pool_size"],  # 连接池大小
        max_overflow=config["max_overflow"],  # 超过连接池大小时,允许的最大连接数
        pool_recycle=3600,  # 连接回收时间(秒)
        pool_timeout=30,  # 连接超时时间(秒)
        echo=False,  # 是否打印SQL语句
    )
    engines[db_name] = engine
    session_factories[db_name] = sessionmaker(bind=engine)

    async_db_url = f"mysql+asyncmy://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset={config['charset']}"
    async_engine = create_async_engine(async_db_url, echo=True)
    async_engines[db_name] = async_engine
    async_session_factories[db_name] = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

Base = declarative_base()


# 获取数据库连接
@contextmanager
def get_db(db_name: str):
    session = session_factories[db_name]()
    try:
        yield session
    finally:
        session.close()


# 通用上下文管理器
class SessionManager:
    def __init__(self, db_name: str):
        self.session_factory = async_session_factories[db_name]

    async def __aenter__(self):
        self.session = self.session_factory()
        await self.session.begin()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()