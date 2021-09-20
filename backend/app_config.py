# Database config
database = 'postgresql'
host = 'localhost'
port = '5432'
user_name = 'postgres'
password = '123456'
database_name = 'test2'

# FastAPI config
title = "Administrative work handling system"
description = """
Administrative work handling system
is a system, which let an organization manages and operates their administrative works
E.g: creating form, form instances, defining workflows,...
"""
origins = [
    "http://localhost:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost"
]
