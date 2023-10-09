# encoding: utf-8
# Filename: resources.py


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.db import get_db
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
    * It could be decided by the `config.py`
    * **:param page**: The page of the posts.
    * **:param db**: Session of the database.
    * **:return**: The dict type data of posts.
    """

    return resource_tools.get_data_of_posts_from_db(page=page, db=db)


@router_resources.get('/posts/get/{post_uuid}')
def get_single_post(post_uuid: str, db: Session = Depends(get_db)):
    pass
