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
    post_uuid: str
    content: str

    class Config:
        from_attributes = True


class UserModify(BaseModel):
    nick_name: str
    description: str

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    new_password: str
    verify_new_password: str
