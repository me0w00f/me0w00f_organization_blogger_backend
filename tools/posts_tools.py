# encoding: utf-8
# Filename: posts_tools.py

from fastapi import HTTPException, UploadFile, File
from pathlib import Path
from sqlalchemy.orm import Session
from model import crud
import config
import shutil

def write_the_post(user_name: str, post_uuid: str, post_file: UploadFile = File()):
    """
    Create the directory for the post.
    :param post_file: File Object.
    :param user_name: Name of user, it cannot be changed.
    :param post_uuid: Uuid of post.
    :return: Result of the operation.
    """

    author_dir = Path(config.STATIC_DIR).joinpath("posts").joinpath(user_name)
    author_post_dir = author_dir.joinpath(post_uuid)

    if not author_dir.mkdir(exist_ok=True):
        HTTPException(
            status_code=500,
            detail=f"Can not create directory {author_dir.name} !"
        )

    if not author_post_dir.mkdir(exist_ok=True):
        HTTPException(
            status_code=500,
            detail=f"Can not create directory {author_post_dir.name} !"
        )
    try:
        with open(str(author_post_dir.joinpath(post_uuid+'.md')), 'w') as f:
            content = post_file.file.read()
            f.write(content.decode('utf-8'))
    except IOError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Can not write posts file {str(author_post_dir.joinpath(post_uuid + '.md'))}! \n {e}"
        )

    return True


def delete_the_post(user_name: str, post_uuid: str):
    author_dir = Path(config.STATIC_DIR).joinpath("posts").joinpath(user_name)
    author_post_dir = author_dir.joinpath(post_uuid)

    try:
        shutil.rmtree(author_post_dir)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return True


def check_if_authorized(author_uuid: str, post_uuid: str, db: Session):
    """
    Check if a post is authorized by a user.
    :param db: Session of the database.
    :param author_uuid: Uuid of the author.
    :param post_uuid: Uuid of the post.
    :return: The result of checking.
    """

    if not crud.check_post_author(author_uuid=author_uuid, post_uuid=post_uuid, db=db):
        return False

    return True
