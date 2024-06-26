from typing import Dict, Any
from utils.consts.codes import *


def make_response(
    data: Any = None, code: int = SUCCESS, message: str = None
) -> Dict[str, Any]:
    if message is None:
        message = ERROR_MESSAGES.get(code, "Unknown error")

    return {
        "data": data,
        "code": code,
        "message": message,
    }
