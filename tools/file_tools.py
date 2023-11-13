# encoding: utf-8
# Filename: file_tools.py

from fastapi import UploadFile
import os
import config
import markdown
import bleach


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


def convert_md_to_html(original_markdown_content: str):
    """
    Convert markDown string content to HTML content.
    :param original_markdown_content: Original sting in markdown format.
    :return: HTML content string.
    """

    html = markdown.markdown(text=original_markdown_content, extensions=['fenced_code', 'codehilite'])

    return html
