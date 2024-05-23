# encoding: utf-8
# Filename: administrator.py

from fastapi import APIRouter, Depends, HTTPException, status

from model import crud
from dependencies.db import get_db
from tools import admin_tools
import config

router_admin = APIRouter(
    prefix='/api/admin',
    tags=['Administration'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "description": "Not Found."
        }
    }
)


@router_admin.get('/users/get')
def get_all_users():
    pass


@router_admin.get('/status')
def status() -> None:
    pass
