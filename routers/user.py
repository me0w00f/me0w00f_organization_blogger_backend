# encoding: utf-8
# Filename: user.py

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status

import config
from model import schemas
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dependencies.db import get_db
from model import crud
from tools import token_tools

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
    * Create a user by providing username, password and email.
    * **:param UserReg**: The information to sign up.
    * **:param db**: Session of database.
    * **:return**: The result of creating.
    """

    if crud.create_user(UserReg=UserReg, db=db):
        return {
            'Status': 'Success!'
        }


@router_user.post('/token')
async def user_login(UserLogin: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    * Login an account by providing username and password, then return a token.
    * **:param UserLogin**: The information to sign in.
    * **:param db**: Session of database.
    * **:return**: Token to authenticate.
    """

    # Authenticate the user using the provided username and password
    user_authentication = token_tools.authenticate_user(
        user_name=UserLogin.user_name, password=UserLogin.password, db=db)

    # If authentication fails, raise an HTTP exception with a 401 Unauthorized status code.
    if not user_authentication:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    try:
        # Get the user's details from the database using their username.
        user = crud.get_user_by_name(user_name=UserLogin.user_name, db=db)

        # Set the expiration time for the access token.
        access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

        # Create the access token with the user's UUID as the subject (sub).
        access_token = token_tools.create_access_token(
            data={"sub": user.user_uuid},
            expires_delta=access_token_expires
        )

    # If there's an error in creating the token, raise an HTTP exception with a 401 Unauthorized status code.
    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Cannot create token.',
            headers={'WWW-Authenticate': 'Bearer'}
        )

    # Return the access token.
    return {'access_token': access_token}
