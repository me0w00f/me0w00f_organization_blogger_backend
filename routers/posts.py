# encoding: utf-8
# Filename: posts.py

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from uuid import uuid4
from sqlalchemy.orm import Session
from dependencies.db import get_db
from dependencies.oauth2scheme import oauth2Scheme
from tools import posts_tools, token_tools, file_tools
from model import crud, schemas
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


@router_posts.post('/create')
async def create_a_post(posts_title: str, tags: str, category_id: int, comment: bool, content_file: UploadFile = File(),
                        token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    * Send a post with a file.
    * :param posts_title: Title of the post.
    * :param tags: Tags of the post.
    * :param category_id: Category of the post.
    * :param comment: Allow to comment or not.
    * :param content_file: Markdown file.
    * :param token: Token of the user.
    * :param db: Session of the database.
    * :return: Response of the server.
    """

    author_uuid = token_tools.get_uuid_by_token(token=token)
    author = crud.get_admin_by_uuid(admin_uuid=author_uuid, db=db)
    post_uuid: str = str(uuid4())

    if not author:
        raise HTTPException(
            status_code=401,
            detail="Permission Denied!"
        )

    if not file_tools.check_file_allowed(upload_file=content_file):
        raise HTTPException(
            status_code=400,
            detail=f"File '{content_file.filename}' is not allowed to upload!"
        )

    if not posts_tools.check_if_category_exists(category_id=category_id, db=db):
        raise HTTPException(
            status_code=400,
            detail=f" Category '{category_id}' does not exist!"
        )

    if not posts_tools.write_the_post(user_name=author.user_name, post_uuid=post_uuid, post_file=content_file):
        raise HTTPException(
            status_code=500,
            detail="Update failed."
        )

    if crud.create_post(post_uuid=post_uuid, posts_title=posts_title, tags=tags,
                        comment=comment, category_id=category_id, user_uuid=author_uuid, db=db):
        return {
            "Status": "Success!"
        }


@router_posts.put('/update')
async def update_a_post(post_uuid: str, posts_title: str, tags: str, category_id: int, comment: bool,
                        new_content_file: UploadFile = File(), token: str = Depends(oauth2Scheme),
                        db: Session = Depends(get_db)):
    """
    * Update a post with new information and a file.
    * :param post_uuid: Uuid of the post.
    * :param posts_title: Title of the post.
    * :param tags: Tags of the post.
    * :param category_id: Category of the post.
    * :param comment: Allow to comment or not.
    * :param new_content_file: Markdown file
    * :param token: Token of the user.
    * :param db: Session of the database.
    * :return: Response of the server.
    """
    author_uuid = token_tools.get_uuid_by_token(token=token)
    author = crud.get_admin_by_uuid(admin_uuid=author_uuid, db=db)

    if not author:
        raise HTTPException(
            status_code=401,
            detail="Permission Denied!"
        )

    if not file_tools.check_file_allowed(upload_file=new_content_file):
        raise HTTPException(
            status_code=400,
            detail=f"File '{new_content_file.filename}' is not allowed to upload!"
        )

    if not posts_tools.check_if_category_exists(category_id=category_id, db=db):
        raise HTTPException(
            status_code=400,
            detail=f" Category '{category_id}' does not exist!"
        )

    if not posts_tools.check_if_authorized(author_uuid=author_uuid, post_uuid=post_uuid, db=db):
        raise HTTPException(
            status_code=400,
            detail=f"The post is not authorized by user '{author.user_name}' !"
        )

    if not posts_tools.write_the_post(user_name=author.user_name, post_uuid=post_uuid, post_file=new_content_file):
        raise HTTPException(
            status_code=500,
            detail="Updating failed."
        )

    if crud.update_post(post_uuid=post_uuid, user_uuid=author_uuid, posts_title=posts_title,
                        tags=tags, category_id=category_id, comment=comment, db=db):
        return {
            "Status": "Success!"
        }


@router_posts.delete('/delete')
async def delete_a_post(post_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Delete a post.
    :param post_uuid: Uuid of the post.
    :param token: Token of the user.
    :param db: Session of the database.
    :return: Session of the database.
    """

    author_uuid = token_tools.get_uuid_by_token(token=token)
    author = crud.get_admin_by_uuid(admin_uuid=author_uuid, db=db)

    if not author:
        raise HTTPException(
            status_code=401,
            detail="Permission Denied!"
        )

    if not posts_tools.check_if_authorized(author_uuid=author_uuid, post_uuid=post_uuid, db=db):
        raise HTTPException(
            status_code=400,
            detail=f"The post is not authorized by user '{author.user_name}' !"
        )

    if not posts_tools.delete_the_post(user_name=author.user_name, post_uuid=post_uuid):
        raise HTTPException(
            status_code=500,
            detail="Deletion failed."
        )

    if crud.delete_post(user_uuid=author.user_uuid, post_uuid=post_uuid, db=db):
        return {
            "Status": "Success!"
        }


@router_posts.post('/categories/create')
def create_categories(category: schemas.Category,
                      token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Create a category.
    :param category: Category name.
    :param token: Token of a user.
    :param db: Session of database.
    :return: Status of the request.
    """

    author_uuid = token_tools.get_uuid_by_token(token=token)
    author = crud.get_admin_by_uuid(admin_uuid=author_uuid, db=db)

    if not author:
        raise HTTPException(
            status_code=401,
            detail="Permission Denied!"
        )

    if crud.create_category_in_db(category=category, db=db):
        return {
            "Status": "Success!"
        }
