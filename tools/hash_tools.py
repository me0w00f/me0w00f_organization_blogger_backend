# encoding: utf-8
# Filename: hash_tools.py

from passlib.context import CryptContext

passwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def get_password_hashed(plain_password: str) -> str:
    """
    Make the password hashed so as not to leak.
    :param plain_password: Password to be hashed.
    :return: The hashed password.
    """
    return passwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the password from the plain to the hashed.
    :param plain_password: The original password.
    :param hashed_password: The hashed password.
    :return: The result of the verification.
    """

    return passwd_context.verify(secret=plain_password, hash=hashed_password)

