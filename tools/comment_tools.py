# encoding: utf-8
# Filename: comment_tools.py

from model import crud, schemas
from sqlalchemy.orm import Session
from fastapi import HTTPException


def create_a_comment(comments: schemas.Comment, user_uuid: str, db: Session):
    """
    Check the exceptions before the data written into database.
    :param comments: Content of the comment.
    :param user_uuid: Uuid of the user.
    :param db: Session of the database.
    :return: Result.
    """

    if not crud.get_single_post_data(post_uuid=comments.post_uuid, db=db):
        raise HTTPException(
            status_code=400,
            detail=f"The post {comments.post_uuid} does not exist!"
        )

    if crud.create_comments_in_db(comments=comments, user_uuid=user_uuid, db=db):

        return True


def load_comments_by_a_post_uuid(post_uuid: str, db: Session):
    """
    Load all comments of a post by providing a post uuid.
    :param post_uuid: Uuid of post.
    :param db: Session of the database.
    :return: All comments of a post.
    """

    return crud.query_all_comments_by_post_uuid(post_uuid=post_uuid, db=db)
