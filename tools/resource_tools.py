# encoding: utf-8
# Filename: resources_tools.py
# Methods of the fetch the resources.

from model import crud
from sqlalchemy.orm import Session


def get_data_of_posts_from_db(page: int, db: Session):
    """
    Get the data of posts from the database.
    :param db: Session of the database.
    :param page: The page of the posts.
    :return: The dict type data of posts.
    """

    return crud.select_all_of_posts_by_page(page=page, db=db)