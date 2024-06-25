from loguru import logger
from config import GlobalConfig
import os
from datetime import datetime

# 创建日志目录
log_dir = GlobalConfig.get_log_path()
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")

# 配置 loguru
logger.remove()  # 移除默认的日志配置

# 定义日志文件路径和格式
log_file_format = os.path.join(log_dir, f"{current_date}_{{level}}.log")

# 配置不同日志等级的文件
logger.add(
    log_file_format.format(level="debug"),
    level="DEBUG",
    rotation="00:00",  # 每天午夜分割日志
    retention="10 days",  # 保留10天的日志
    compression="zip",  # 压缩日志文件
)

logger.add(
    log_file_format.format(level="info"),
    level="INFO",
    rotation="00:00",
    retention="10 days",
    compression="zip",
)

logger.add(
    log_file_format.format(level="error"),
    level="ERROR",
    rotation="00:00",
    retention="10 days",
    compression="zip",
)

log = logger
