# encoding: utf-8
# Filename: file_tools.py

from fastapi import UploadFile
import os
import config


def check_posts_file_allowed(upload_file: UploadFile):
    """
    Check if the posts file allowed to be uploaded.
    :return: Bool, the result of the checking.
    """

    file_extension = os.path.splitext(upload_file.filename)

    return file_extension[1] in config.ALLOWED_TYPE


def check_image_file_allowed(upload_file: UploadFile):
    """
    Check if the image file allowed to be uploaded.
    :return: Bool, the result of the checking.
    """

    file_extension = os.path.splitext(upload_file.filename)

    return file_extension[1] in config.ALLOWED_IMAGE
