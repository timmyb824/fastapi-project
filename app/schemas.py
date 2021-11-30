from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# defined schema with pydantic; class should always be capitalized
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# inherits from PostBase; pass gives it the same fields as PostBase
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created: datetime
    user_id: int

    # required by fastapi to convert to JSON
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Response class for when a user is created
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
