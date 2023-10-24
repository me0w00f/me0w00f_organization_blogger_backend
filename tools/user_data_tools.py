# encoding: utf-8
# Filename: user_data_tools.py
import os

from fastapi import UploadFile, File, HTTPException
from pathlib import Path
import config
import random
import os


def create_user_directory(user_uuid: str):
    """
    Create a directory for new user and named after uuid.
    :param user_uuid: Uuid of the user.
    :return:
    """

    # Generate the directory address of the user.
    user_dir = Path(config.STATIC_DIR).joinpath('users').joinpath(user_uuid)

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

    original_avatar_path = Path(config.STATIC_DIR)\
        .joinpath('users')\
        .joinpath(user_uuid)

    file_extension = os.path.splitext(avatar_file.filename)
    avatar_file_list = os.listdir(original_avatar_path)

    try:
        if len(avatar_file_list) != 0:
            for i in avatar_file_list:
                os.remove(original_avatar_path.joinpath(i))
        with open(original_avatar_path.joinpath('0' + file_extension[1]), 'wb') as f:
            content = avatar_file.file.read()
            f.write(content)
            return True
    except IOError as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


