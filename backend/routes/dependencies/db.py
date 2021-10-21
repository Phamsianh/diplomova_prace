from ORM.engine import engine
from sqlalchemy.orm import sessionmaker


def get_session():
    # we must create new session for each request, otherwise session will be cached
    ss = sessionmaker()
    session = ss(bind=engine, autoflush=False)
    try:
        yield session
    finally:
        session.close()
