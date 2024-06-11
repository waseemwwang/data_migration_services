import toml
import os

from loguru import logger


global_config = {}


class GlobalConfig:

    def __init__(self):
        logger.debug("Global config initializing...")
        try:
            global global_config
            deploy = os.environ.get("DEPLOY", "dev")
            global_config = toml.load(f"./config_{deploy}.toml")
            logger.debug(f"Config is {global_config}")
            logger.debug("Config loaded successfully.")
        except (FileNotFoundError, toml.TomlDecodeError) as e:
            logger.error(f"Failed to load config: {e}")
            # 可以考虑在这里设置默认配置值或退出程序

    @classmethod
    def get_reload(cls) -> bool:
        return global_config.get("base", {}).get("reload", True)

    @classmethod
    def get_port(cls) -> int:
        return global_config.get("base", {}).get("port", 8080)

    @classmethod
    def get_log_level(cls) -> str:
        return global_config.get("base", {}).get("log_level", "info")

    @classmethod
    def get_database_mysql(cls):
        return global_config.get("database", {}).get("mysql", {})

    @classmethod
    def get_log_path(cls):
        return global_config.get("base", {}).get("log_path", "logs")


global_config_instance = GlobalConfig()
