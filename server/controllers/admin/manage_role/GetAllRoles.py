from controllers.auth.AuthBase import AuthBase
from ORM.session import session
from ORM.Model.Role import Role


class GetAllRoles(AuthBase):
    def get(self):
        if self.is_auth():
            self.res["role"] = self.get_role()

            if self.is_admin():
                role = []
                for r in session.query(Role).all():
                    role.append({
                        "role_id": r.id,
                        "name": r.name,
                        # "permission": str(r.permission)
                    })

                self.res["data"] = role
                self.write(self.res)
            else:
                self.write(self.res)