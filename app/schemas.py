from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

# defined schema with pydantic; class should always be capitalized
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# inherits from PostBase; pass gives it the same fields as PostBase
class PostCreate(PostBase):
    pass

# Response class for when a user is created
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created: datetime

    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created: datetime
    user_id: int
    user: UserOut

    # required by fastapi to convert to JSON
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # less than or equal to 1 (allows negative numbers unfortunately)
