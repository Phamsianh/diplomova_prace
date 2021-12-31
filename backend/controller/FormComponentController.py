from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class FormComponentController(BaseController):
    def patch_rsc_ins(self, rsc_ins, req_body):
        if rsc_ins.public or rsc_ins.obsolete:
            raise ORMExc.ORMException("form's currently public or obsolete")
        else:
            return super().patch_rsc_ins(rsc_ins, req_body)

    def delete_rsc_ins(self, rsc_ins):
        if rsc_ins.public or rsc_ins.obsolete:
            raise ORMExc.IndelibleResourceInstance
        else:
            return super().delete_rsc_ins(rsc_ins)
