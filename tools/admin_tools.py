# encoding: utf-8
# Filename: admin_tools.py

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from model import crud, schemas
from dependencies.db import engine
from tools import user_data_tools
import json

get_db = sessionmaker(bind=engine)


def create_administrator(db: Session = get_db()):
    """
    Create administrators from the JSON list.
    :param db: Session of the database.
    :return: Status of the Operation.
    """
    try:
        with open('admin_list.json', 'r') as f:
            administrators_to_create = json.load(f)
            for administrator in administrators_to_create:
                admin_reg = schemas.UserReg(
                    user_name=administrator['user_name'],
                    password=administrator['password'],
                    email=administrator['email'])
                if crud.create_admin(db=db, AdminReg=admin_reg):
                    admin_uuid = crud.get_admin_by_name(
                        db=db,
                        admin_name=admin_reg.user_name).user_uuid
                    if not user_data_tools.create_user_directory(user_uuid=admin_uuid):
                        raise HTTPException(
                            status_code=500,
                            detail="Cannot create user directory!")
                    print(f'Administrator {admin_reg.user_name} created!')

    except IntegrityError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
