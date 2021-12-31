from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class PositionController(BaseController):
    def delete_rsc_ins(self, rsc_ins):
        if rsc_ins.holders is not None:
            raise ORMExc.IndelibleResourceInstance
        else:
            super().delete_rsc_ins(rsc_ins)
