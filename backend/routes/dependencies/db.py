from ORM.session import session
from ORM import event_handler


def get_session():
    try:
        yield session
    finally:
        session.close()
