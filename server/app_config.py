import path

# Database config
database = 'postgresql'
host = 'localhost'
port = '5432'
user_name = 'postgres'
password = '123456'
database_name = 'test'

# App setting
settings = {
    'template_path': path.views_path,
    # 'autoreload': True,
    'static_path': path.static_path,
    'cookie_secret': 'this is random value1',
}

title = 'This is title'