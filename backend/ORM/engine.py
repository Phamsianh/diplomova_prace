from sqlalchemy import create_engine
from app_config import database, host, port, user_name, password, database_name

uri = f'{database}://{user_name}:{password}@{host}:{port}/{database_name}'

# SQLAlchemy 1.4 now has compilation caching system.
# more detail in: https://docs.sqlalchemy.org/en/14/core/connections.html#sql-caching
# and in:  https://docs.sqlalchemy.org/en/14/faq/performance.html#why-is-my-application-slow-after-upgrading-to-1-4-and-or-2-x

engine = create_engine(uri, echo=True)
