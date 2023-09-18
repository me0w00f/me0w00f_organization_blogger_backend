"""
Main entrance.

The main execution of the project.

"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from routers import user
from model import crud, models, schemas
from dependencies.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router_user)


@app.get("/")
def root():
    """
    Return some information about the server.
    :return: Information of the server.
    """
    return {
        "Message": {
            "Project": "Me0W00f Blogger API",
            "Version": "1.0 alpha",
            "Powered by": "FastAPI",
            "Server date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
