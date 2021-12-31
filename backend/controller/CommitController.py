from typing import Union

from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class CommitController(BaseController):
    def get_rsc_ins(self, rsc_id: Union[str, int]):
        rsc_ins = self.session.query(self.model).get(rsc_id)
        if not rsc_ins:
            raise ORMExc.ResourceInstanceNotFound(self.model, rsc_id)
        else:
            return rsc_ins

    def post_rsc_ins(self, req_body):
        """
        Commit cannot be created create manually. It's created when user transit instance to next phase
        """
        raise ORMExc.ORMException("Commit cannot be created manually."
                                  " It's created when user transit instance to next phase")

    def patch_rsc_ins(self, rsc_ins, req_body):
        """
        Commit cannot be modify.
        """