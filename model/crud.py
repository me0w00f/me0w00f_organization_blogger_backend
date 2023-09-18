from sqlalchemy.orm import Session
from uuid import uuid4
from . import models, schemas
import time


def create_user(UserReg: schemas.UserReg, db: Session) -> dict:
    """
    Create a user with information provided in database.
    :param UserReg: The information to sign up.
    :param db: Session of database.
    :return: The result of operation.
    """
    # Generate the datetime of creating the user.
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # Generate the uuid of the user.
    user_uuid = str(uuid4())
    db_user = models.User(
        user_name=UserReg.user_name,
        password=UserReg.password,
        email=UserReg.email,
        date=date,
        user_uuid=user_uuid,
        nick_name=UserReg.user_name,
    )

    db.add(db_user)
    db.commit()
    db.refresh()

    return db_user


def get_user_by_name():
    """
    Check if the username provided exists,
    but it is only used by registering the user.
    :return:
    """


def get_user_by_uuid():
    """
    Check if the user exists in a database,
    it is usually used to authenticate.
    :return:
    """
    pass


def get_admin_by_name():
    """
    Check if the username provided exists, but it is only used by registering the user.
    :return:
    """
    pass


def get_admin_by_uuid():
    """
    Check if the user exists in a database,
    it is usually used to authenticate.
    :return:
    """
    pass

