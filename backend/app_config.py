import os

############################## DATABASE CONFIG ##############################
# For development, use the following config for database:
# database = 'postgresql'
# host = 'localhost'
# port = '5432'
# user_name = 'postgres'
# password = '123456'
# database_name = 'test2'

# For using with docker, use the following config for database:
database = os.environ.get('DB')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
user_name = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
database_name = os.environ.get('DB_NAME')

############################## FASTAPI CONFIG ##############################
# For development comment out the api_root_path.
api_root_path = os.environ.get('API_ROOT_PATH')
title = "Information System for Supporting Administration Process (ISSAP)"
description = """
ISSAP is information system created for supporting administration process.
It allows user to create an administration process, define phases and transitions with a form for user to intantiate.
ISSAP also audit all content before user transit instance to the next phase. Audit trail is used for administrative purposes.
"""
servers = [
    {'url': 'http://localhost:8000/', 'description': 'Development server'},
    {'url': 'http://localhost/api/', 'description': 'Production server'}
]
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://editor.swagger.io"
]

############################## TOKEN USING FOR AUTHENTICATION ##############################
SECRET_KEY = "5c303030e2c614051f0787b0a6250615247be31677e92f21afc210d2d4607c18"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200  #  = 30*24*60 = 1 month
