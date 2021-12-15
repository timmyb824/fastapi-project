import pytest
from jose import jwt
from app import schemas
from app.config import settings
# from .database import client, session # not needed anymore since this is specified in conftest.py

# def test_root(client):
#     res = client.get("/")
#     # print(res)
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Welcome to my first API!'
#     assert res.status_code == 200


# addition trailing '/' prevents test from failing due to 307 redirect
def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    # assert res.json().get("email") == "hello123@gmail.com"

    # ** unpacks the dictionary
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user,client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200