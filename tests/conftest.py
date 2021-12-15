# this is a special pytest file for defining fixtures
# fixtures will automatically be accessible by all tests in this package
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app

from app.config import settings
from app.database import get_db
from app.database import Base
# from alembic import command

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    # print("my session scope='fixture' ran") # scopes can be set such as session(scope="module")
    Base.metadata.drop_all(bind=engine) # running it here allows you to see data in db after each test
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