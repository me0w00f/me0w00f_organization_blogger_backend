# encoding: utf-8
# Filename: models.py

from sqlalchemy import Column, INT, VARCHAR, TEXT, DATETIME, BOOLEAN
from dependencies.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(INT, primary_key=True, index=True, autoincrement=True)
    user_uuid = Column(VARCHAR(36), unique=True, nullable=False)
    user_name = Column(VARCHAR(32), unique=True, nullable=False)
    nick_name = Column(VARCHAR(255), nullable=False)
    password = Column(TEXT, nullable=False)
    email = Column(VARCHAR(64), unique=True, nullable=False)
    description = Column(TEXT, nullable=False, default="这个人很懒，什么都没有留下。")
    administrator = Column(BOOLEAN, nullable=False, default=False)
    date = Column(DATETIME, nullable=False)


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(INT, primary_key=True, index=True, autoincrement=True)
    post_uuid = Column(VARCHAR(36), unique=True, nullable=False)
    title = Column(TEXT, nullable=False)
    author_uuid = Column(VARCHAR(36), nullable=False)
    tags = Column(TEXT, nullable=False)
    category_id = Column(INT, nullable=False)
    comment = Column(BOOLEAN, nullable=False)
    date = Column(DATETIME, nullable=False)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(INT, primary_key=True, autoincrement=True)
    category_name = Column(TEXT, unique=True, nullable=False)
    datetime = Column(DATETIME, nullable=False)


class Comments(Base):
    __tablename__ = 'comments'
    id = Column(INT, primary_key=True, autoincrement=True)
    comment_uuid = Column(VARCHAR(36), unique=True, nullable=False)
    post_uuid = Column(VARCHAR(36), nullable=False)
    user_uuid = Column(VARCHAR(36), nullable=False)
    content = Column(TEXT, nullable=False)
    date = Column(DATETIME, nullable=False)
