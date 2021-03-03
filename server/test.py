from ORM.session import session
from ORM.Model.User import User
from ORM.Model.Role import Role

user = session.query(User).filter_by(id=1).first()


# print(user.form_structures)
print(user.user_roles[0].role.permission[0])
# print(user)

