from controllers.auth.AuthBase import AuthBase
from ORM.session import session
from ORM.Model.FormStructure import FormStructure
import json


class CreateFormStructure(AuthBase):
    def initialize(self):
        super().initialize()
        self.error = {}
        self.valid = True

    def get(self):
        self.render(r"form_structure\create.html")

    def post(self):
        if self.is_auth():
            self.res['role'] = self.get_role()

            if self.is_admin():

                self.check_name(self.get_body_argument('name'))
                self.check_structure(self.get_body_argument('structure'))
                self.check_admin_digital_signature(self.get_body_argument('admin_digital_signature'))

                if self.valid:
                    self.res["data"] = {
                        "name": self.get_body_argument('name'),
                        "structure": json.loads(self.get_body_argument('structure')),
                        "admin_digital_signature": self.get_body_argument('admin_digital_signature')
                    }
                else:
                    self.res["error"] = self.error

                self.write(self.res)
            else:
                self.write(self.res)

    def check_name(self, name):
        if not name:
            self.valid = False
            self.error["name"] = "Name Empty"
            return None
        elif session.query(FormStructure).filter_by(name=name).count():
            self.valid = False
            self.error["name"] = "Name existed"
            return None
        else:
            return True

    def check_structure(self, structure):
        try:
            s = json.loads(structure)
        except:
            self.valid = False
            self.error["structure"] = "invalid structure"
            return False
        else:
            return True

    def check_admin_digital_signature(self, s):
        return True