from pydantic import BaseModel


class UserReg(BaseModel):
    user_name: str
    password: str
    email: str

    class Config:
        orm_mode=True


class Posts(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Category(BaseModel):
    category_name: str

    class Config:
        orm_mode = True


class UserModify(BaseModel):
    nick_name: str
    description: str

    class Config:
        orm_mode = True
