from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class FormComponentController(BaseController):
    def patch_rsc_ins(self, rsc_ins, req_body):
        """To patch form's component (phase, section, field):

        * Form must not be obsolete
        """
        if rsc_ins.obsolete:
            raise ORMExc.ORMException("form's currently obsolete")
        return super().patch_rsc_ins(rsc_ins, req_body)

    def delete_rsc_ins(self, rsc_ins):
        """To delete form's component (phase, section, field):

        * Form must not be public or obsolete
        """
        if rsc_ins.public or rsc_ins.obsolete:
            raise ORMExc.IndelibleResourceInstance
        return super().delete_rsc_ins(rsc_ins)
