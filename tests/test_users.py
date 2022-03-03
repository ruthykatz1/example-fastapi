from fastapi.testclient import TestClient
from app5.main import app
from app5 import schemas

from app5.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app5.database import get_db
from app5.database import Base

import pytest

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base.metadata.create_all(bind=engine)

# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Hello World successfully deployed from CI/CD pipeline"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email":"hello123@gmail.com", "password":"password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201