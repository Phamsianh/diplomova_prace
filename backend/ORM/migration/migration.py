from ORM.Base import Base
from ORM.engine import engine
import ORM.Model
import os

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    os.system('python -m ORM.migration.seed_users')
    os.system('python -m ORM.migration.seed_forms')
