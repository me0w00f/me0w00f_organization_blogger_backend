# encoding: utf-8
# Filename: comments.py

from fastapi import APIRouter, Depends, HTTPException, status

from model import schemas
from sqlalchemy.orm import Session
from dependencies.db import get_db
from dependencies.oauth2scheme import oauth2Scheme
from tools import comment_tools, token_tools
import config


router_comments = APIRouter(
    prefix='/api/comments',
    tags=['Comments'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "description": 'Not found.'
        }
    }
)


@router_comments.post('/send')
def send_comments(comments: schemas.Comment, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Send a comment to server.
    :param comments: Content of the comment, it is an object.
    :param token: Token of the user.
    :param db: Session of the database.
    :return: Result.
    """
    user_uuid = token_tools.get_uuid_by_token(token=token)

    if comment_tools.create_a_comment(comments=comments, user_uuid=user_uuid, db=db):

        return {
            "Status": "Success!"
        }


@router_comments.get('/get_in_a_post')
def get_all_comments_in_a_post(post_uuid: str, db: Session = Depends(get_db)):
    """
    Get all the comments from a post by providing a uuid.
    :param post_uuid: Uuid of post.
    :param db: Session of the database.
    :return: Status of response.
    """

    return comment_tools.load_comments_by_a_post_uuid(post_uuid=post_uuid, db=db)

