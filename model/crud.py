# encoding: utf-8
# Filename: crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from tools.hash_tools import get_password_hashed
from . import models, schemas
import time


def create_user(UserReg: schemas.UserReg, db: Session) -> dict | bool:
    """
    Create a user with information provided in the database.
    :param UserReg: Information to sign up.
    :param db: Session of database.
    :return: Result of operation.
    """

    # Check if user exists
    existing_user = get_user_by_name(db=db, user_name=UserReg.user_name)
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail='User has already existed!'
        )

    # Check if email has already used.
    existing_email = db.query(models.User).filter(models.User.email == UserReg.email).first()
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail='Email has already been used!'
        )

    # Generate the datetime of creating the user.
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Generate the uuid of the user.
    user_uuid = str(uuid4())

    # Generate the hashed password
    hashed_password = get_password_hashed(plain_password=UserReg.password)

    # Create the column of the user.
    db_user = models.User(
        user_name=UserReg.user_name,
        password=hashed_password,
        email=UserReg.email,
        date=date,
        user_uuid=user_uuid,
        nick_name=UserReg.user_name,
        administrator=False  # New users are not admins by default
    )

    try:

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return db_user


def create_admin(db: Session, AdminReg: schemas.UserReg) -> dict:
    """
    Create an admin with the information provided in the database.
    :param AdminReg: Information to sign up.
    :param db: Session of database.
    :return: Result of operation.
    """

    # Check if user exists
    existing_admin = get_admin_by_name(db=db, admin_name=AdminReg.user_name)
    if existing_admin:
        raise HTTPException(
            status_code=409,
            detail='User has already existed!'
        )

    # Check if email has already used.
    existing_email = db.query(models.User).filter(models.User.email == AdminReg.email).first()
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail='Email has already been used!'
        )

    # Generate the datetime of creating the admin.
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # Generate the uuid of the admin.
    admin_uuid = str(uuid4())

    # Generate the hashed password
    hashed_password = get_password_hashed(plain_password=AdminReg.password)

    # Create the column of the admin.
    db_admin = models.User(
        user_name=AdminReg.user_name,
        password=hashed_password,
        email=AdminReg.email,
        date=date,
        user_uuid=admin_uuid,
        nick_name=AdminReg.user_name,
        administrator=True
    )

    try:

        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return db_admin


def get_user_by_name(db: Session, user_name: str):
    """
    Get a user from the database by their username.
    :param db: Session of database.
    :param user_name: The name of the user.
    :return: The user if they exist, None otherwise.
    """
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def get_user_by_uuid(db: Session, user_uuid: str):
    """
    Check if the user exists in a database,
    it is usually used to authenticate.
    :param db: Session of the database.
    :param user_uuid: The uuid of the user.
    :return: The user if they exist, None otherwise.
    """

    return db.query(models.User).filter(models.User.user_uuid == user_uuid).first()


def get_admin_by_name(db: Session, admin_name: str):
    """
    Get an admin from the database by their username.
    :param db: Session of database.
    :param admin_name: The name of the admin.
    :return: The admin if they exist, None otherwise.
    """

    return db.query(models.User).filter(
        models.User.user_name == admin_name,
        models.User.administrator == True
    ).first()


def get_admin_by_uuid(db: Session, admin_uuid: str):
    """
    Get an admin from the database by their uuid.
    :param db: Session of database.
    :param admin_uuid: The uuid of the admin.
    :return: The admin if they exist, None otherwise.
    """

    return db.query(models.User).filter(
        models.User.user_uuid == admin_uuid,
        models.User.administrator == True
    ).first()
