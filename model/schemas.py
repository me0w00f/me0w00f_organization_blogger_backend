# encoding: utf-8
# Filename: schemas.py

from pydantic import BaseModel


class UserReg(BaseModel):
    user_name: str
    password: str
    email: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    user_name: str
    password: str

    class Config:
        from_attributes = True


class Posts(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class Category(BaseModel):
    category_name: str

    class Config:
        from_attributes = True


class UserModify(BaseModel):
    nick_name: str
    description: str

    class Config:
        from_attributes = True
