import uvicorn
from config import GlobalConfig


if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host="0.0.0.0",
        port=GlobalConfig.get_port(),
        reload=GlobalConfig.get_reload(),
        log_level=GlobalConfig.get_log_level(),
    )
