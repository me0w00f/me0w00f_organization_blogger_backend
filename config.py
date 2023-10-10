# encoding: utf-8
# Filename: config.py


# Main

STATIC_DIR = 'static'

# Database
DATABASE_URL = "mysql://me0w00f:me0w00f@localhost/me0w00f"
RESOURCES_POSTS_LIMIT = 10

# Authenticate

SECRET_KEY = 'weepingdogel'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Uploading

ALLOWED_TYPE = ['.md', '.markdown']

