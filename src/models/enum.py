from enum import Enum


class ChatbotUserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"