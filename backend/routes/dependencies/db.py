from ORM.engine import engine
from ORM.session import Session


def get_session():
    # we must create new session for each request, otherwise session will be cached
    # ss = sessionmaker()
    session = Session(bind=engine, autoflush=False, expire_on_commit=False)
    try:
        yield session
    finally:
        session.close()
