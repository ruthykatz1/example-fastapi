from fastapi.testclient import TestClient
from app5.main import app

from app5.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app5.database import get_db
from app5.database import Base

import pytest
from app5.oauth2 import create_access_token
from app5 import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_user(client):
    user_data = {"email":"someone@gamil.com", "password":"123"}
    res = client.post("/users/", json=user_data)
    new_user = res.json() #The returned json doesn't include the password
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"someone123@gamil.com", "password":"123"}
    res = client.post("/users/", json=user_data)
    new_user = res.json() #The returned json doesn't include the password
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()

    return session.query(models.Post).all()