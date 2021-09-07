from sqlalchemy import create_engine
from app_config import database, host, port, user_name, password, database_name

uri = f'{database}://{user_name}:{password}@{host}:{port}/{database_name}'

engine = create_engine(uri, echo=True)
