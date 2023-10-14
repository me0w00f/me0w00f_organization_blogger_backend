# encoding: utf-8
# Filename: user_data_tools.py

from pathlib import Path
import config


def create_user_directory(user_uuid: str):
    """
    Create a directory for new user and named after uuid.
    :param user_uuid:
    :return:
    """
    user_dir = Path(config.STATIC_DIR).joinpath(user_uuid)

    try:

        user_dir.mkdir(exist_ok=True)
        return True

    except IOError:

        return False
