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

    def check_structure(self, s):
        try:
            structure = json.loads(s)
        except:
            self.valid = False
            self.error["structure"] = "invalid structure"
            return False
        else:
            self.structure_must_be_list(structure)
            if not self.valid:
                return False
            else:
                for i in range(len(structure)):
                    section = structure[i]
                    if self.valid:
                        self.section_must_be_dict(section, i)
                    else: continue
                    if self.valid:
                        self.section_contain_right_fields(section, i, right_fields=[
                            "section_name",
                            "permission",
                            "fields",
                            "description",
                            "digital_signature"
                        ])
                    else: continue
                    if self.valid:
                        self.all_right_fields_is_required(section, i)
                    else: continue
                if not self.valid: return False
                else: return True

    def structure_must_be_list(self, structure):
        if type(structure) is not list or len(structure) == 0:
            self.valid = False
            self.error["structure"] = "structure must be an array and must not be empty"
            return False
        else:
            return True

    def section_must_be_dict(self, section, i):
        if type(section) is not dict or len(section) == 0:
            self.valid = False
            self.error["structure"] = { f"section_{i}": "section must be a JSON and must not be empty"}
            return False
        else:
            return True

    def section_contain_right_fields(self, section, i, right_fields):
        wrong_fields = []
        for field in section:
            if field not in right_fields:
                self.valid = False
                wrong_fields.append(field)
        if not self.valid:
            self.error["structure"] = {
                f"section_{i}": f'''contain other field '{', '.join(wrong_fields)}' among {', '.join(right_fields)}'''
            }
            return False
        else: return True

    def all_right_fields_is_required(self, section, i):
        self.error[f"section_{i}"] = {}
        if "section_name" not in section or len(section["section_name"]) == 0:
            self.valid = False
            self.error[f"section_{i}"]["section_name"] = "section name is required"
        if "permission" not in section or len(section["permission"]) == 0:
            self.valid = False
            self.error[f"section_{i}"]["permission"] = "permission is required"
        if "fields" not in section or len(section["fields"]) == 0:
            self.valid = False
            self.error[f"section_{i}"]["fields"] = "field is required"
        if "description" not in section or len(section["description"]) == 0:
            self.valid = False
            self.error[f"section_{i}"]["description"] = "description is required"
        if "digital_signature" not in section or len(section["digital_signature"]) == 0:
            self.valid = False
            self[f"section_{i}"]["digital_signature"] = "digital signature is required"

        if self.valid:
            self.error.pop(f"section_{i}")
            return True
        else: return False

    def check_admin_digital_signature(self, s):
        return True

    # er = {
    #     "structure": {
    #         "section_1":{
    #             "name": "Name is required",
    #             "permission": "permission is required",
    #             "fields": {
    #                 "fields_name": "data type does not support"
    #             },
    #             "description": "",
    #             "digital_signature": "digital signature is required"
    #         }
    #     }
    # }