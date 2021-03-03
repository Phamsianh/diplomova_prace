from tornado.web import RequestHandler
from ORM.Model.User import User
from ORM.session import session
import hashlib
import re

class ResetPassword(RequestHandler):
    def initialize(self):
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.flag = True
        self.error = {}

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

    def get(self):
        self.render(r'auth\resetpassword.html')

    def post(self):
        if self.current_user:
            self.check_current_password(self.get_argument('current_password'))
            self.check_new_password(self.get_argument('new_password'), self.get_argument('confirm_password'))

            if self.flag:
                self.write({
                    "auth": True,
                    "reset_password": True,
                })
            else:
                self.write({
                    "auth": True,
                    "reset_password": False,
                    "error": self.error
                })
        else:
            self.write({
                "auth": False
            })

    def check_current_password(self, current_pw):
        hash_current_pw = hashlib.sha256(current_pw.encode()).hexdigest()
        if self.current_user.password == hash_current_pw:
            return True
        else:
            self.flag = False
            self.error['current_password'] = 'Wrong current password'
            return False

    def check_new_password(self, new_pw, confirm_pw):
        error = ""
        flag = True

        if new_pw != confirm_pw:
            self.error["confirm_password"] = "New password and confirm password are not the same"
            flag = False

        if len(new_pw) < 8:
            error += 'Password too short. '
            flag = False

        if not re.search(r'[a-z]', new_pw) :
            error += 'Missing lowcase character from a to z. '
            flag = False

        if not re.search(r'[A-Z]', new_pw):
            error += 'Missing uppercase character from A to Z. '
            flag = False

        if not re.search(r'[@#$%^&+=.]', new_pw):
            error += 'Missing special character from @#$%^&+=. '
            flag = False

        if flag:
            return True
        else:
            self.flag = False
            error = error[:0] +\
                    "Password must contain at least 8 charater, includes A-Z, a-z, 0-9 and special character. " +\
                    error[0:]
            self.error['new_password'] = error
            return False
