from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class InstanceFieldController(BaseController):
    def post_rsc_ins(self, req_body):
        raise ORMExc.ORMException("resource can not be created manually")

    def patch_rsc_ins(self, rsc_ins, req_body):
        current_handlers = rsc_ins.instance.curr_handlers
        if self.cur_usr not in current_handlers:
            raise ORMExc.ORMException("you're not current handlers of this phase")
        else:
            return super().patch_rsc_ins(rsc_ins, req_body)

    def delete_rsc_ins(self, rsc_ins):
        raise ORMExc.IndelibleResourceInstance()

# Instance field cannot be updated by participants if they are not handlers of current phase

