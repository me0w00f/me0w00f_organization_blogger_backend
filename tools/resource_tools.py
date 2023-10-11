# encoding: utf-8
# Filename: resources_tools.py
# Methods of the fetch the resources.

from fastapi import HTTPException
from model import crud
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import config


def get_data_of_posts_from_db(page: int, db: Session):
    """
    Get the data of posts from the database.
    :param db: Session of the database.
    :param page: The page of the posts.
    :return: The dict type data of posts.
    """

    return crud.select_all_of_posts_by_page(page=page, db=db)


def get_data_of_single_post_from_db(post_uuid: str, db: Session):
    """
    Get the data of a single post from the database.
    :param post_uuid: Uuid of the post.
    :param db: Session of the database.
    :return: The dict type data of a single post.
    """

    return crud.get_single_post_data(post_uuid=post_uuid, db=db)


def read_post_content(post_uuid: str, author_name: str):
    """
    Read the content of the post file.
    :param author_name: Name of the author
    :param post_uuid: Uuid of the post.
    :return:
    """

    author_dir = Path(config.STATIC_DIR).joinpath("posts")
    post_dir = author_dir.joinpath(author_name).joinpath(post_uuid).joinpath(post_uuid + '.md')
    try:
        with open(post_dir) as f:

            return f.read()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
