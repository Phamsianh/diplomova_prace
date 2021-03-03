from tornado.web import RequestHandler
from ORM.Model.User import User
from ORM.Model.UserRole import UserRole
from ORM.session import session
import hashlib
import re


class Register(RequestHandler):
    def initialize(self):
        self.error = dict()
        self.valid = True
        self.set_header('Access-Control-Allow-Origin', '*')

    def get(self):
        self.render(r'auth\register.html')

    def post(self):
        data = {
            'first_name': self.get_body_argument('first_name'),
            'last_name': self.get_body_argument('last_name'),
            'user_name': self.get_body_argument('user_name'),
            'email': self.get_body_argument('email'),
            'password': self.get_body_argument('password'),
            'confirm_password': self.get_body_argument('confirm_password'),
            'phone': self.get_body_argument('phone'),
        }
        if self.validate(data):
            # self.redirect('/login')
            self.write({'register': True})
        else:
            self.write({
                'register': False,
                'error': self.error
            })

    def validate(self, data):
        self.check_first_name(data['first_name'])
        self.check_last_name(data['last_name'])
        self.check_user_name(data['user_name'])
        self.check_email(data['email'])
        self.check_password(data['password'], data['confirm_password'])

        if self.valid:
            user = User(
                first_name= data['first_name'],
                last_name= data['last_name'],
                user_name= data['user_name'],
                email= data['email'],
                password= hashlib.sha256(data['password'].encode()).hexdigest(),
                phone= data['phone']
            )

            session.add(user)
            session.commit()

            user_id = session.query(User).filter_by(email=data['email']).first().id
            user_role = UserRole(user_id=user_id, role_id=3)
            session.add(user_role)
            session.commit()
            return True
        else:
            return False

    def check_first_name(self, first_name):
        if not first_name:
            self.error['first_name'] = 'First name empty'
            self.valid = False
            return False
        else:
            return True

    def check_last_name(self, last_name):
        if not last_name:
            self.error['last_name'] = 'Last name empty'
            self.valid = False
            return False
        else:
            return True

    def check_user_name(self, user_name):
        if not session.query(User).filter_by(user_name=user_name).first():
            return True
        else:
            self.error['user_name'] = 'User name already existed'
            self.valid = False
            return False

    def check_email(self, email):
        flag = True

        # check email format
        email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not re.search(email_regex, email):
            self.error['email'] = 'Invalid email'
            self.valid = False
            flag = False

        # check email unique
        elif session.query(User).filter_by(email=email).first():
            self.error['email'] = 'Email already existed'
            self.valid = False
            flag = False

        return flag

    def check_password(self, password, confirm_password):
        error = ""
        flag = True

        if password != confirm_password:
            self.error["confirm_password"] = "New password and confirm password are not the same"
            flag = False

        if len(password) < 8:
            error += 'Password too short. '
            flag = False

        if not re.search(r'[a-z]', password) :
            error += 'Missing lowcase character from a to z. '
            flag = False

        if not re.search(r'[A-Z]', password):
            error += 'Missing uppercase character from A to Z. '
            flag = False

        if not re.search(r'[@#$%^&+=.]', password):
            error += 'Missing special character from @#$%^&+=. '
            flag = False

        if flag:
            return True
        else:
            self.valid = False
            error = error[:0] +\
                    "Password must contain at least 8 charater, includes A-Z, a-z, 0-9 and special character. " +\
                    error[0:]
            self.error['new_password'] = error
            return False


    def check_phone(self, phone):
        pass
