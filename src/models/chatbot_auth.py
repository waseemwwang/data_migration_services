from datetime import datetime, UTC
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    DECIMAL,
    Enum,
    ForeignKey,
    VARBINARY,
    Text,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.inspection import inspect
from models.database import Base


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    deleted_at = Column(DateTime, nullable=True)


class PrintableMixin:
    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return str(self.as_dict())


class ChatbotUser(Base, TimestampMixin, PrintableMixin):
    """问答机器人用户表"""

    __tablename__ = "chatbot_user"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), index=True, nullable=False)
    alias = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    role = Column(Enum("admin", "user"), nullable=False)
    project = relationship("ChatbotUserProjectPermission", back_populates="user")


class ChatbotUserProjectPermission(Base, TimestampMixin, PrintableMixin):
    """问答机器人用户项目权限表"""

    __tablename__ = "chatbot_user_project_permission"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("chatbot_user.id"), index=True, nullable=False)
    project_id = Column(Integer, index=True, nullable=False)
    project_name = Column(String(60), index=True, nullable=False)
    is_owner = Column(Boolean, default=False)

    user = relationship("ChatbotUser", uselist=False, back_populates="project")

