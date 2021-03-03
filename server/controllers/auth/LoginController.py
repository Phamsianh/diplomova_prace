from tornado.web import RequestHandler
from ORM.Model.User import User
from ORM.session import session
import hashlib
import re
import json


class Login(RequestHandler):
    def initialize(self):
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.error = dict()
        self.flag = True
        self.user = User()

    def get(self):
        self.render(r'auth\login.html')
        # self.write({"login": "please login"})

    def post(self):
        email_or_username = self.get_body_argument('email')
        password = self.get_body_argument('password')
        hash_pw = hashlib.sha256(password.encode()).hexdigest()

        if re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email_or_username):
            email = email_or_username
            self.check_email(email)
            if self.flag:
                self.check_password(hash_pw)
        else:
            user_name = email_or_username
            self.check_user_name(user_name)
            if self.flag:
                self.check_password(hash_pw)

        if self.flag:
            self.set_secure_cookie(name="user_id", value=str(self.user.id), expires_days=30)
            self.write({
                'auth': True,
                # 'user': {
                #     'id': self.user.id,
                #     'first_name': self.user.first_name,
                #     'last_name': self.user.last_name,
                #     'user_name': self.user.user_name,
                #     'email': self.user.email,
                #     'phone': self.user.phone
                # }
            })
            # self.redirect('/')
        else:
            self.write({
                'auth': False,
                'error': self.error
            })

    def check_user_name(self, user_name):
        user = session.query(User).filter_by(user_name=user_name).first()
        if user:
            self.user = user
            return True
        else:
            self.error['email'] = "User name is not existed"
            self.flag = False
            return False

    def check_email(self, email):
        user = session.query(User).filter_by(email=email).first()
        if user:
            self.user = user
            return True
        else:
            self.error['email'] = "Email is not existed"
            self.flag = False
            return False

    def check_password(self, password):
        if self.user.password == password:
            return True
        else:
            self.error['password'] = 'Password is wrong'
            self.flag = False
            return False