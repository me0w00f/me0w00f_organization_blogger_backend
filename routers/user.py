from fastapi import APIRouter, Depends, HTTPException
from model import schemas
from sqlalchemy.orm import Session
from dependencies.db import get_db

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
def create_user(UserReg: schemas.UserReg, db: Session = Depends(get_db)):
    """
    Create a user by providing username, password and email.
    :param UserReg: The information to sign up.
    :param db: Session of database.
    :return: The result of creating.
    """


