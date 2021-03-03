from controllers.auth.AuthBase import AuthBase
from ORM.session import session
from ORM.Model.FormStructure import FormStructure
import json


class GetAllFormStructures(AuthBase):
    def get(self):
        if self.is_auth():
            self.res["role"] = self.get_role()

            if self.is_admin():
                form_structures = []
                for fs in session.query(FormStructure).all():
                    form_structures.append({
                        "user_id": fs.user_id,
                        "name": fs.name,
                        "structure": json.loads(fs.structure),
                        "admin_digital_signature": fs.admin_digital_signature
                    })

                self.res["data"] = form_structures
                self.write(self.res)
            else:
                self.write(self.res)