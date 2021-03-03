from ORM.Model.UserRole import UserRole
from ORM.Model.User import User
from ORM.Model.Role import Role
from ORM.session import session

user_1_role_admin = UserRole(user_id=1, role_id=1)
user_2_role_staff = UserRole(user_id=2, role_id=2)
user_3_role_client = UserRole(user_id=3, role_id=3)


session.add_all([user_1_role_admin,user_2_role_staff,user_3_role_client])
session.commit()