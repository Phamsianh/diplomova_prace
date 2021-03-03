from tornado.web import RequestHandler
from ORM.Model.User import User
from ORM.session import session


class Home(RequestHandler):
    def initialize(self):
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:3000')
        self.set_header("Access-Control-Allow-Credentials", 'true')

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
        if self.current_user:
            data = {
                'user_id': self.current_user.id,
                'user_name': self.current_user.user_name
            }
            self.write({
                'auth': True,
                'data': data
            })
        else:
            self.write({
                'auth': False,
            })
