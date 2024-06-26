import toml
import os


global_config = {}


class GlobalConfig:

    def __init__(self):
        try:
            global global_config
            deploy = os.environ.get("DEPLOY", "dev")
            global_config = toml.load(f"./config_{deploy}.toml")
        except (FileNotFoundError, toml.TomlDecodeError) as e:
            # 可以考虑在这里设置默认配置值或退出程序
            pass

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
    def get_database_mysql_by_type(cls, type: str = "base"):
        return global_config.get("database", {}).get("mysql", {}).get(type, {})

    @classmethod
    def get_database_mysql(cls):
        return global_config.get("database", {}).get("mysql", {})

    @classmethod
    def get_log_path(cls):
        return global_config.get("base", {}).get("log_path", "logs")


global_config_instance = GlobalConfig()
