from tornado.web import RequestHandler
from ORM.Model.User import User
from ORM.Model.Role import Role
from ORM.session import session


class AuthBase(RequestHandler):
    def initialize(self):
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.set_header("Access-Control-Allow-Credentials", 'true')
        self.res = {}

    def get_current_user(self):
        if self.get_secure_cookie("user_id"):
            user_id = int(self.get_secure_cookie("user_id"))
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                return user
            else:
                return None
        else:
            return None

    def is_auth(self):
        if self.current_user:
            self.res["auth"] = True
            return True
        else:
            self.res["auth"] = False
            return False

    def get_role(self):
        if self.current_user is not None:
            roles = []
            for user_role in self.current_user.user_roles:
                roles.append(user_role.role.name)
            return roles
        else:
            print('current user is none')
            return none

    def is_admin(self):
        if self.current_user is not None:
            flag = False
            for user_role in self.current_user.user_roles:
                if user_role.role_id == 1:
                    flag = True
            return flag
        else:
            print('current user is none')
            return False