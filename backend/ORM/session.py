from ORM.engine import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()
session = Session(bind=engine, autoflush=False)
