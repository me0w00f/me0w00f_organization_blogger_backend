# encoding: utf-8
# Filename: comments.py

from fastapi import APIRouter, Depends, HTTPException, status

from model import schemas
from sqlalchemy.orm import Session
from dependencies.db import get_db
from dependencies.oauth2scheme import oauth2Scheme
from tools import comment_tools
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


@router_comments.get('/get_all')
def get_all_comments_in_a_post():
    pass
