from typing import Union

from ORM.session import session
from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class UserController(BaseController):
    def get_rsc_ins(self, rsc_id: Union[str, int]):
        if rsc_id == 'me':
            rsc_ins = self.cur_usr
        elif type(rsc_id) == str:
            rsc_ins = self.session.query(self.model).filter(self.model.user_name == rsc_id).first()
        else:
            rsc_ins = super().get_rsc_ins(rsc_id)
        if rsc_ins is None:
            raise ORMExc.ResourceInstanceNotFound(self.model, rsc_id)
        else:
            return rsc_ins

    def post_rsc_ins(self, req_body):
        """
        TODO:
        Create new user include:\n
        1.  validate req_body:
            *  username must be unique
            *  password must long enough (length?), include alphanumeric characters and specialized characters.
        2.  initialize new user:
            *  create new user
            *  create asymmetric key pair for sign and encrypt/decrypt instance's contents.
        """
        return super().post_rsc_ins(req_body)

    def delete_rsc_ins(self, rsc_ins):
        raise ORMExc.IndelibleResourceInstance


if __name__ == '__main__':
    uc1 = UserController(session=session)
    uc1.post_rsc_ins(req_body={

    })
