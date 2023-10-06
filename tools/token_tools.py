# encoding: utf-8
# Filename: token_tools.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from tools.hash_tools import verify_password
from model import crud
import config


def authenticate_user(user_name: str, password: str, db: Session):
    """
    Authenticate a user by user_name and password.
    :param user_name: user_name, a string type data.
    :param password: Password inputted from frontend.
    :param db: Session of the database.
    :return: The result of the authentication.
    """

    # Query the user in the database.
    user = crud.get_user_by_name(user_name=user_name, db=db)

    # Check if the user exists.
    # If not, return the False.
    # If so, the check if the password is correct.
    if not user:
        return False
    elif not verify_password(password, user.password):
        return False

    # If everything is ok, then return True.
    return True


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Function to create a JWT (JSON Web Token) with a custom expiration time.

    :param data: The data to be included in the token.
    :param expires_delta: The amount of time until the token expires. If not provided, defaults to 15 minutes.
    :return: The encoded JWT as a string.
     """

    # Copying the data dictionary to ensure the original is not modified.
    to_encode = data.copy()

    # Checking if an expiration time delta was provided.
    # If an expiration time delta is provided, calculate the expiration time by adding it to the current time.
    # If no expiration time delta is provided, set the expiration time to 15 minutes from now by default.

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # Adding the expiration time to the data to be encoded
    to_encode.update({
        "exp": expire
    })

    # Encoding the data into a JWT using the secret key and the specified algorithm from the configuration.
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, config.ALGORITHM
    )

    # Returning the encoded JWT
    return encoded_jwt


def get_uuid_by_token(token: str):
    """
    Get uuid by token.
    :param token: Token to get uuid.
    :return: return a uuid.
    """

    try:
        data_decoder = jwt.decode(token=token, key=config.SECRET_KEY, algorithms=config.ALGORITHM)
        user_uuid: str = data_decoder.get('sub')

        if user_uuid is None:
            return False
        return user_uuid

    except JWTError:
        return False
