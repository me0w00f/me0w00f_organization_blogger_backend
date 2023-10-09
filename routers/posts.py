# encoding: utf-8
# Filename: posts.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from uuid import uuid4
from sqlalchemy.orm import Session
from dependencies.db import get_db
from dependencies.oauth2scheme import oauth2Scheme
from tools import posts_tools, token_tools
from model import crud
import config

router_posts = APIRouter(
    prefix='/api/posts',
    tags=['Posts'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "description": 'Not found.'
        }
    }
)


@router_posts.post('/send')
def send_a_post(posts_title: str, tags: str, category_id: int, comment: bool, content_file: UploadFile = File(),
                token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    * Send a post with a file.
    * :param posts_title: Title of the post.
    * :param tags: Tags of the post.
    * :param category_id: Category of the post.
    * :param comment: Allow to comment or not.
    * :param content_file: Markdown file
    * :param token: Token of the user
    * :param db: Session of the database.
    * :return: Response of the server.
    """

    author_uuid = token_tools.get_uuid_by_token(token=token)
    author = crud.get_admin_by_uuid(admin_uuid=author_uuid, db=db)
    post_uuid = str(uuid4())
    if not author:
        raise HTTPException(
            status_code=401,
            detail="Permission Denied!"
        )

    posts_tools.write_the_post(user_name=author.user_name, post_uuid=post_uuid, post_file=content_file)

    if crud.create_post(post_uuid=post_uuid, posts_title=posts_title, tags=tags,
                        comment=comment, category_id=category_id, user_uuid=author_uuid, db=db):

        return {
            "Status": "Success!"
        }


@router_posts.put('/update')
def update_a_post(post_uuid: str, new_content_file: UploadFile, token: str = Depends(oauth2Scheme),
                  db: Session = Depends(get_db)):
    pass


@router_posts.delete('/delete')
def delete_a_post(post_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    pass
