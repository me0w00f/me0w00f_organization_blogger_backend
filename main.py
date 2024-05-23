# encoding: utf-8
# Filename: main.py

"""
Main entrance.

The main execution of the project.

"""
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path
from tools import admin_tools
from routers import user, resources, posts, administrator, comments
from model import crud, models, schemas
from dependencies.db import SessionLocal, engine
import config

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router_user)
app.include_router(resources.router_resources)
app.include_router(posts.router_posts)
app.include_router(administrator.router_admin)
app.include_router(comments.router_comments)

static_path = Path(config.STATIC_DIR)
user_path = Path(config.STATIC_DIR + '/users')
posts_path = Path(config.STATIC_DIR + '/posts')
static_path.mkdir(exist_ok=True)
user_path.mkdir(exist_ok=True)
posts_path.mkdir(exist_ok=True)

app.mount('/static', StaticFiles(directory=config.STATIC_DIR), name='static')

admin_tools.create_administrator()


@app.get("/")
def root():
    """
    * Return some information about the server.
    * :return: Information of the server.
    """
    return {
        "Message": {
            "Project": "Me0W00f Blogger API",
            "Version": "1.0 alpha",
            "Powered by": "FastAPI",
            "Server date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }


