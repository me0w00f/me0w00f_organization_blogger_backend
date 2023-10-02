# encoding: utf-8
# Filename: user.py

from fastapi import APIRouter, Depends, HTTPException
from model import schemas
from sqlalchemy.orm import Session
from dependencies.db import get_db
from model import crud

router_user = APIRouter(
    prefix='/api/user',
    tags=['Users'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            'description': 'Not found.'
        }
    }
)


@router_user.post('/sign_up')
async def create_user(UserReg: schemas.UserReg, db: Session = Depends(get_db)):
    """
    Create a user by providing username, password and email.
    :param UserReg: The information to sign up.
    :param db: Session of database.
    :return: The result of creating.
    """

    if crud.create_user(UserReg=UserReg, db=db):

        return {
            'Status': 'Success!'
        }


@router_user.post('/token')
async def authenticate_user(UserLogin: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Login an account by providing username and password, then return a token.
    :param UserLogin: The information to sign in.
    :param db: Session of database.
    :return: Token to authenticate.
    """
