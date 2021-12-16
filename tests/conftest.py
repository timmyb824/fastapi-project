# this is a special pytest file for defining fixtures
# fixtures will automatically be accessible by all tests in this package
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.oauth2 import create_access_token
from app.config import settings
from app.database import get_db
from app.database import Base
from app import models
# from alembic import command

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    # print("my session scope='fixture' ran") # scopes can be set such as session(scope="module")
    Base.metadata.drop_all(bind=engine) # running it here allows you to see data in db after each test since db is not deleted until next tests is run
    Base.metadata.create_all(bind=engine)
    # command.upgrade("head") # if we wanted to use alembic
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# client function will call session function before it runs
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db

    # return new TestClient
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "timothy@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

#############################################################################################

@pytest.fixture
def test_user2(client):
    user_data = {"email": "timothy123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    # map(function, list_data)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    # could have used this method to add posts to db
    # session.add_all([models.Post(title="first title", content="first content", user_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", user_id=test_user['id']), models.Post(title="3rd title", content="3rd content", user_id=test_user['id'])])
    # session.commit()
    # session.query(models.Post).all()

    session.commit()
    posts = session.query(models.Post).all()
    return posts