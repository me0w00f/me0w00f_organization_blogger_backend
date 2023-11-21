# encoding: utf-8
# Filename: crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from uuid import uuid4

from model.models import User, Posts, Category, Comments
from tools.hash_tools import get_password_hashed
from . import schemas
from datetime import datetime
import config


def create_user(UserReg: schemas.UserReg, db: Session) -> dict | bool:
    """
    Create a user with information provided in the database.
    :param UserReg: Information to sign up.
    :param db: Session of database.
    :return: Result of operation.
    """

    # Check if user exists
    existing_user = get_user_by_name(db=db, user_name=UserReg.user_name)
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail='User has already existed!'
        )

    # Check if email has already used.
    existing_email = db.query(User).filter(User.email == UserReg.email).first()
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail='Email has already been used!'
        )

    # Generate the datetime of creating the user.
    date = datetime.utcnow()

    # Generate the uuid of the user.
    user_uuid = str(uuid4())

    # Generate the hashed password
    hashed_password = get_password_hashed(plain_password=UserReg.password)

    # Create the column of the user.
    db_user = User(
        user_name=UserReg.user_name,
        password=hashed_password,
        email=UserReg.email,
        date=date,
        user_uuid=user_uuid,
        nick_name=UserReg.user_name,
        administrator=False  # New users are not admins by default
    )

    try:

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return db_user


def create_admin(db: Session, AdminReg: schemas.UserReg) -> dict:
    """
    Create an admin with the information provided in the database.
    :param AdminReg: Information to sign up.
    :param db: Session of database.
    :return: Result of operation.
    """

    # Check if user exists
    existing_admin = get_admin_by_name(db=db, admin_name=AdminReg.user_name)
    if existing_admin:
        raise HTTPException(
            status_code=409,
            detail='User has already existed!'
        )

    # Check if email has already used.
    existing_email = db.query(User).filter(User.email == AdminReg.email).first()
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail='Email has already been used!'
        )

    # Generate the datetime of creating the admin.
    date = datetime.utcnow()

    # Generate the uuid of the admin.
    admin_uuid = str(uuid4())

    # Generate the hashed password
    hashed_password = get_password_hashed(plain_password=AdminReg.password)

    # Create the column of the admin.
    db_admin = User(
        user_name=AdminReg.user_name,
        password=hashed_password,
        email=AdminReg.email,
        date=date,
        user_uuid=admin_uuid,
        nick_name=AdminReg.user_name,
        administrator=True
    )

    try:

        db.add(db_admin)
        db.commit()
        db.refresh(db_admin)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return db_admin


def create_post(post_uuid: str, user_uuid: str, posts_title: str, tags: str, category_id: int,
                comment: bool, db: Session):
    """
    Create a data of a post in the database.
    :param post_uuid: Uuid of the post.
    :param user_uuid: Uuid of the user.
    :param posts_title: Title of the post.
    :param tags: Tags of the post.
    :param category_id: Category of the post.
    :param comment: Allow to comment or not.
    :param db: Session of the database.
    :return: Result of operation.
    """

    date = datetime.utcnow()

    db_posts = Posts(
        post_uuid=post_uuid,
        title=posts_title,
        author_uuid=user_uuid,
        category_id=category_id,
        tags=tags,
        comment=comment,
        create_time=date,
        update_time=date
    )

    try:
        db.add(db_posts)
        db.commit()
        db.refresh(db_posts)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    return db_posts


def update_post(post_uuid: str, user_uuid: str, posts_title: str, tags: str, category_id: int,
                comment: bool, db: Session):
    """
    Update a post.
    :param post_uuid: Uuid of the post.
    :param user_uuid: Uuid of the user.
    :param posts_title: Title of the post.
    :param tags: Tags of the post.
    :param category_id: Category of the post.
    :param comment: Allow to comment or not.
    :param db: Session of the database.
    :return:
    """
    update_date = datetime.utcnow()

    try:
        status: int = db.query(Posts) \
            .filter(Posts.post_uuid == post_uuid, Posts.author_uuid == user_uuid) \
            .update(
            {
                'title': posts_title,
                'tags': tags,
                'category_id': category_id,
                'comment': comment,
                'update_time': update_date
            },
            synchronize_session="evaluate")

        if status == 0:
            return False

        db.commit()

        return True

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def delete_post(post_uuid: str, user_uuid: str, db: Session):
    """
    Delete a post.
    :param post_uuid: Uuid of the post.
    :param user_uuid: Uuid of the user.
    :param db: Session of the database.
    :return:
    """

    db_delete_post = db.query(Posts) \
        .filter(Posts.post_uuid == post_uuid, Posts.author_uuid == user_uuid).first()

    try:
        db.delete(db_delete_post)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def create_comments_in_db(comments: schemas.Comment, user_uuid: str, db: Session):
    """
    Create a comment in the database.
    :param user_uuid: Uuid of the user.
    :param comments: Content of the comment, it is an object.
    :param db: Session of the database.
    :return: Result.
    """
    date = datetime.utcnow()
    comment_uuid = str(uuid4())

    db_comments = Comments(
        comment_uuid=comment_uuid,
        post_uuid=comments.post_uuid,
        user_uuid=user_uuid,
        content=comments.content,
        date=date
    )

    try:
        db.add(db_comments)
        db.commit()
        db.refresh(db_comments)

        return True

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def create_category_in_db(category: schemas.Category, db: Session):
    """
    Create a category in the database.
    :param category: Category name.
    :param db: Session of database.
    :return: Result.
    """
    date = datetime.utcnow()

    db_category = Category(
        category_name=category.category_name,
        datetime=date
    )

    try:
        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        return True

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(f"{category.category_name} has already existed!", str(e))
        )


def get_user_by_name(user_name: str, db: Session):
    """
    Get a user from the database by their username.
    :param db: Session of database.
    :param user_name: The name of the user.
    :return: The user if they exist, None otherwise.
    """
    return db.query(User).filter(User.user_name == user_name).first()


def get_user_by_uuid(db: Session, user_uuid: str):
    """
    Check if the user exists in a database,
    it is usually used to authenticate.
    :param db: Session of the database.
    :param user_uuid: The uuid of the user.
    :return: The user if they exist, None otherwise.
    """

    return db.query(User).filter(User.user_uuid == user_uuid).first()


def get_admin_by_name(db: Session, admin_name: str):
    """
    Get an admin from the database by their username.
    :param db: Session of database.
    :param admin_name: The name of the admin.
    :return: The admin if they exist, None otherwise.
    """

    return db.query(User).filter(
        User.user_name == admin_name,
        User.administrator == True
    ).first()


def get_admin_by_uuid(admin_uuid: str, db: Session):
    """
    Get an admin from the database by their uuid.
    :param db: Session of database.
    :param admin_uuid: The uuid of the admin.
    :return: The admin if they exist, None otherwise.
    """

    return db.query(User).filter(
        User.user_uuid == admin_uuid,
        User.administrator == True
    ).first()


def get_category_name(category_id: int, db: Session):
    """
    Get the name of category by ID.
    :param category_id: ID of the category.
    :param db: Session of database.
    :return: The name of category by ID.
    """
    return db.query(Category).filter(Category.id == category_id).first()


def check_post_author(author_uuid: str, post_uuid: str, db: Session):
    """
    Check if a post is authorized by a user by querying the database.
    :param author_uuid: Uuid of the author.
    :param post_uuid: Uuid of the post.
    :param db: Session of the database.
    :return: The result of querying.
    """

    return db.query(Posts) \
        .filter(Posts.post_uuid == post_uuid, Posts.author_uuid == author_uuid).first()


def select_all_of_posts_by_page(page: int, db: Session):
    """
    Function to retrieve posts from the database, paginated by the given page number.
    Return 10 items of the posts by default.
    It could be decided by the `config.py`.
    :param page:
    :param db:
    :return: The list type data of posts.
    """

    # Get the maximum amount posts to retrieve per page from the configuration.
    posts_select_limit: int = config.RESOURCES_POSTS_LIMIT

    # Calculate the offset for the database query based on the page number and posts limit.
    page_db: int = (page - 1) * posts_select_limit

    # Query the database for posts, ordered by date in descending order.
    # Limit the amount results by the posts limit and offset the results by the calculated offset.
    # Return all results as a list.

    return db.query(Posts) \
        .order_by(desc(Posts.create_time)) \
        .limit(posts_select_limit).offset(page_db).all()


def get_single_post_data(post_uuid: str, db: Session):
    """
    Get the data of a single post from the database.
    :param post_uuid: Uuid of the post.
    :param db: Session of the database.
    :return: The dict type data of a single post.
    """

    return db.query(Posts).filter(Posts.post_uuid == post_uuid).first()


def get_all_categories_in_db(db: Session):
    """
    Get all the categories from the database.
    :param db: Session of the database.
    :return: Return the data of all the categories.
    """

    return db.query(Category.id, Category.category_name)


def get_category_in_db(category_id: int, db: Session):
    """
    Get a category_name in the database.
    :param category_id: ID of the category.
    :param db: Session of the database.
    :return: Result.
    """

    return db.query(Category.category_name).filter(Category.id == category_id).first()


def query_all_comments_by_post_uuid(post_uuid: str, db: Session) -> list[type(Comments)]:
    """
    Query the data of all comments by a post uuid.
    :param post_uuid: Uuid of post.
    :param db: Session of the database.
    :return:
    """

    try:
        # Query the comments.
        db_comments = db.query(Comments).order_by(desc(Comments.date)).filter(Comments.post_uuid == post_uuid).all()
        return db_comments
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
