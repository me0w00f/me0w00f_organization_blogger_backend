# encoding: utf-8
# Filename: comments.py

from fastapi import APIRouter, Depends

from model import schemas, crud
from sqlalchemy.orm import Session
from dependencies.db import get_db
from dependencies.oauth2scheme import oauth2Scheme
from tools import comment_tools, token_tools
from pathlib import Path
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


@router_comments.get('/get_in_a_post/{post_uuid}')
def get_all_comments_in_a_post(post_uuid: str, db: Session = Depends(get_db)):
    """
    Get all the comments from a post by providing a uuid.
    :param post_uuid: Uuid of post.
    :param db: Session of the database.
    :return: Status of response.
    """
    comment_list_for_return: list[dict] = []
    db_comment = comment_tools.load_comments_by_a_post_uuid(post_uuid=post_uuid, db=db)

    for x in db_comment:
        nick_name = crud.get_user_by_uuid(db=db, user_uuid=x.user_uuid).nick_name
        avatar_dir = Path(config.STATIC_DIR).joinpath('users', x.user_uuid)
        avatar_filename = list(avatar_dir.glob("*.*"))[0]
        temp_dict = {
            "id": x.id,
            "comment_uuid": x.comment_uuid,
            "post_uuid": x.post_uuid,
            "user_uuid": x.user_uuid,
            "nick_name": nick_name,
            "avatar": "/" + str(avatar_filename),
            "content": x.content,
            "date": x.date
        }

        comment_list_for_return.append(temp_dict)

    return comment_list_for_return
