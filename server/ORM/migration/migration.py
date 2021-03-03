from ORM.Base import Base
from ORM.engine import engine
from ORM.Model import User, FormStructure, Role, UserRole, Permission, Blockchain,  FormTemplate1
import os

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    os.system('python seed_users.py')
    os.system('python seed_roles.py')
    os.system('python seed_users_roles.py')