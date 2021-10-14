from ORM.session import session


def get_session():
    try:
        yield session
    finally:
        session.close()
