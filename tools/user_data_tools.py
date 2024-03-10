# encoding: utf-8
# Filename: user_data_tools.py

from model import schemas, crud
from fastapi import UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import config
import random


def create_user_directory(user_uuid: str):
    """
    Create a directory for new user and named after uuid.
    :param user_uuid: Uuid of the user.
    :return:
    """

    # Generate the directory address of the user.
    user_dir = Path(config.STATIC_DIR).joinpath('users', user_uuid)

    # Create the directory.
    try:
        user_dir.mkdir(exist_ok=True)
        return True

    except IOError:

        return False


def upload_user_avatar(user_uuid: str, avatar_file: UploadFile = File()):
    """
    Save and compress the avatar of the user.
    :return:
    """
    # Define the original path.
    original_avatar_path = Path(config.STATIC_DIR).joinpath('users', user_uuid)

    # Get the extension of the file.
    file_extension = Path(avatar_file.filename).suffix
    avatar_file_list = list(original_avatar_path.glob("*.*"))

    # Deal with the file of avatar.
    try:
        # Delete the file of old avatar
        if len(avatar_file_list) != 0:
            for i in avatar_file_list:
                i.unlink(missing_ok=True)
        # Write the file of new avatar.
        with original_avatar_path.joinpath("0" + str(random.randint(10000, 99999)) + file_extension).open("wb") as f:
            content = avatar_file.file.read()
            f.write(content)
            return True

    # Deal with errors.
    except IOError as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def update_user_info(user_uuid: str, user_info_modified: schemas.UserModify, db: Session):
    """
    Update the nick_name and description for a user.
    :param user_uuid: UUID of the user.
    :param user_info_modified:  New information of user in request body.
    :param db: Session of the database.
    :return: Status of the operation.
    """

    new_nick_name: str = user_info_modified.nick_name
    new_description: str = user_info_modified.description

    if crud.update_the_nick_name_by_uuid(user_uuid=user_uuid, new_nick_name=new_nick_name, db=db) and \
            crud.update_the_description_by_uuid(new_description=new_description, user_uuid=user_uuid, db=db):
        return True


def password_modify(user_uuid: str, password_modified: schemas.PasswordChange, db: Session):
    """
    Update the password for a user.
    :param user_uuid: UUID of the user.
    :param password_modified: New password of the user in request body.
    :param db: Session of the database.
    :return: Status of the operation.
    """

    if password_modified.new_password == password_modified.verify_new_password:
        if crud.update_password(user_uuid=user_uuid, new_password=password_modified.new_password, db=db):
            return True

    return False
