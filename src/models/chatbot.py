from datetime import datetime
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


class PrintableMixin:
    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return str(self.as_dict())


class Project(Base, PrintableMixin):
    __tablename__ = "Project"

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String(255), nullable=False, primary_key=True)
    parent_id = Column(Integer, nullable=False, default=0)
    outsource_id = Column(VARBINARY(255), nullable=True)
    supplier_company_id = Column(
        Integer,
        ForeignKey("SupplierCompany.supplier_company_id"),
        nullable=True,
        index=True,
    )
    source_code = Column(Integer, nullable=True)
    project_owner_id = Column(Integer, nullable=True, index=True)
    project_owner_name = Column(
        String(255),
        ForeignKey("ProjectOwner.project_owner_name"),
        nullable=True,
        index=True,
    )
    project_model = Column(String(255), nullable=True)
    project_location = Column(String(255), nullable=True)
    project_owner = relationship(
        "ProjectOwner", uselist=False, back_populates="project"
    )
    # project_kick_off_date = Column(DateTime, nullable=True)


class ProjectOwner(Base, PrintableMixin):
    """项目负责人信息"""

    __tablename__ = "ProjectOwner"

    project_owner_id = Column(Integer, primary_key=True, autoincrement=True)
    project_owner_name = Column(String(255), nullable=True, index=True)
    project_owner_alias = Column(String(255), nullable=True)
    project_owner_email = Column(String(255), nullable=True)
    created_time = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="project_owner")

    # 定义联合索引
    __table_args__ = (
        Index("project_owner_id", "project_owner_id", "project_owner_name"),
    )
