import os

# Database config
database = 'postgresql'
host = 'localhost'
port = '5432'
user_name = 'postgres'
password = '123456'
database_name = 'test2'
# database = os.environ.get('DB')
# host = os.environ.get('DB_HOST')
# port = os.environ.get('DB_PORT')
# user_name = os.environ.get('DB_USERNAME')
# password = os.environ.get('DB_PASSWORD')
# database_name = os.environ.get('DB_NAME')

# FastAPI config
title = "Information System for Supporting Administration Process (ISSAP)"
description = """
ISSAP is information system created for supporting administration process.
It allows user to create an administration process, define phases and transitions with a form for user to intantiate.
ISSAP also audit all content before user transit instance to the next phase. Audit trail is used for administrative purposes.
"""
origins = [
    "http://localhost:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost",
    "http://localhost:3000"
]

# token
SECRET_KEY = "5c303030e2c614051f0787b0a6250615247be31677e92f21afc210d2d4607c18"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  #  = 30*24*60 = 1 month
