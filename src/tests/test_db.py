import pytest
from fastapi.testclient import TestClient
from app import app
from models.database import get_db
from models.chatbot import Project, ProjectOwner


client = TestClient(app)


@pytest.fixture(scope="module")
def db_engines():
    with get_db("chatbot") as session:
        yield session


def test_get_all_projects(db_engines):
    projects = db_engines.query(Project).all()
    assert len(projects) > 0


def test_get_project_by_id(db_engines):
    project = db_engines.query(Project).filter(Project.project_id == 40000).first()
    assert project is not None
