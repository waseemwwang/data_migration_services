from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import GlobalConfig
from logger import log

# 数据库连接配置
DB_CONFIG = GlobalConfig.get_database_mysql()
log.debug(f"db config {DB_CONFIG}")

# 创建数据库连接池
engine = create_engine(
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}",
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 超过连接池大小时,允许的最大连接数
    pool_recycle=3600,  # 连接回收时间(秒)
    pool_timeout=30,  # 连接超时时间(秒)
    echo=False,  # 是否打印SQL语句
)

# 创建会话工厂
SessionFactory = sessionmaker(bind=engine)

# 创建声明式基类
Base = declarative_base()


# 获取数据库连接
def get_db_connection():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
