# encoding: utf-8
# Filename: schemas.py

from pydantic import BaseModel


class UserReg(BaseModel):
    user_name: str
    password: str
    email: str

    class Config:
        from_attributes = True


class Category(BaseModel):
    category_name: str

    class Config:
        from_attributes = True


class Comment(BaseModel):
    content: str

    class Config:
        from_attributes = True


class UserModify(BaseModel):
    nick_name: str
    description: str

    class Config:
        from_attributes = True
