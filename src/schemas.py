from pydantic import BaseModel
from typing import Optional, List
import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role_id: Optional[int] = None

class User(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int

class Post(PostBase):
    id: int
    created_at: datetime.datetime
    user_id: int

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    user_id: int
    post_id: int

class Comment(CommentBase):
    id: int
    created_at: datetime.datetime
    user_id: int
    post_id: int

    class Config:
        orm_mode = True
