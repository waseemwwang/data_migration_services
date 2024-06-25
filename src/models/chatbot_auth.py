from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, DECIMAL, Enum, ForeignKey, VARBINARY, Text, Index
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class ChatbotUser(Base, TimestampMixin):
    """问答机器人用户表"""
    __tablename__ = "chatbot_user"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), index=True, nullable=False)
    alias = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    role = Column(Enum('admin', 'user'), nullable=False)


class ChatbotUserProjectPermission(Base, TimestampMixin):
    """问答机器人用户项目权限表"""
    __tablename__ = "chatbot_user_project_permission"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('chatbot_user.id'), index=True, nullable=False)
    project_id = Column(Integer, index=True, nullable=False)
    project_name = Column(String(60), index=True, nullable=False)
    is_owner = Column(Boolean, default=False)
