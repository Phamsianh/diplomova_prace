from controllers.auth.AuthBase import AuthBase
import json


class CreateFormStructure(AuthBase):
    def get(self):
        pass

    def post(self):
        if self.is_auth():
            self.res['role'] = self.get_role()
            if self.is_admin():
                name = self.get_body_argument('name')
                structure = json.loads(self.get_body_argument('structure'))
                admin_digital_signature = self.get_body_argument('admin_digital_signature')

                if self.check_structure(structure):
                    pass

                self.res["data"] = {
                    "name": name,
                    "structure": structure,
                    "admin_digital_signature": admin_digital_signature
                }
                self.write(self.res)
            else:
                self.write(self.res)

    def check_structure(self, structure):
        return True