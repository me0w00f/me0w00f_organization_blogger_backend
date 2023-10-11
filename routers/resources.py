# encoding: utf-8
# Filename: resources.py


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.db import get_db
from model import crud
from tools import resource_tools

router_resources = APIRouter(
    prefix='/api/resources',
    tags=['Resources'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            'description': 'Not Found.'
        }
    }
)


@router_resources.get('/posts/{page}')
def get_posts(page: int, db: Session = Depends(get_db)):
    """
    * Get the data of posts.
    * Each page will return 10 items of the posts by default.
    * It could be decided by the `config.py`.
    * **:param page**: The page of the posts.
    * **:param db**: Session of the database.
    * **:return**: The dict type data of posts.
    """

    data_from_db = resource_tools.get_data_of_posts_from_db(page=page, db=db)
    list_for_return: list[dict] = []

    for x in data_from_db:

        author = crud.get_user_by_uuid(user_uuid=x.author_uuid, db=db)
        category_name = crud.get_category_name(category_id=x.category_id, db=db).category_name
        temp_dict: dict = {
            'id': x.id,
            'post_uuid': x.post_uuid,
            'title': x.title,
            'author_uuid': x.author_uuid,
            'author_name': author.nick_name,
            'tags': x.tags,
            'category_id': x.category_id,
            'category': category_name,
            'comment': x.comment,
            'create_time': x.create_time,
            'update_time': x.update_time
        }

        list_for_return.append(temp_dict)

    return list_for_return


@router_resources.get('/posts/get/{post_uuid}')
def get_single_post(post_uuid: str, db: Session = Depends(get_db)):
    """
    Get a single post by uuid.
    :param post_uuid: Uuid of the post.
    :param db: Session of the database.
    :return: Content, information of the post.
    """
    db_post_info = resource_tools.get_data_of_single_post_from_db(post_uuid=post_uuid, db=db)
    author = crud.get_user_by_uuid(user_uuid=db_post_info.author_uuid, db=db)
    category_name = crud.get_category_name(category_id=db_post_info.category_id, db=db).category_name
    post_content = resource_tools.read_post_content(post_uuid=post_uuid, author_name=author.user_name)

    post_info = {
        "id": db_post_info.id,
        "post_uuid": db_post_info.post_uuid,
        "title": db_post_info.title,
        "tags": db_post_info.tags,
        "author_uuid": db_post_info.author_uuid,
        "author": author.nick_name,
        "category_id": db_post_info.category_id,
        "category": category_name,
        "comment": db_post_info.comment,
        "create_time": db_post_info.create_time,
        "update_time": db_post_info.update_time
    }

    return [post_info, post_content]
