from controllers.auth.AuthBase import AuthBase
from ORM.Model.User import User
from ORM.session import session


class GetAllUsers(AuthBase):
    def get(self):
        if self.is_auth():
            self.res["role"] = self.get_role()

            if self.is_admin():
                users = []
                for user in session.query(User).all():
                    users.append({
                        "user_id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "phone": user.phone
                    })

                self.res["data"] = users
                self.write(self.res)
            else:
                self.write(self.res)