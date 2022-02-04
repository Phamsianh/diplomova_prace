from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class FormController(BaseController):

    def patch_rsc_ins(self, rsc_ins, req_body):
        """Constraint when public form:
        1. Only 1 begin phase and 1 end phase
        2. Each phase must at least has 1 section, each section must at least has 1 field.
        3. Phase must belong
        """
        if 'public' in req_body and req_body['public']:
            if len(rsc_ins.begin_phases) != 1 or len(rsc_ins.end_phases) != 1:
                raise ORMExc.ORMException("form must have 1 begin phase and 1 end phase")
            for p in rsc_ins.phases:
                for s in p.sections:
                    if not s.fields:
                        raise ORMExc.ORMException("Each phase must at least has 1 section,"
                                                  " and each section must at least has 1 field.")

        if 'obsolete' in req_body and req_body['obsolete'] and not rsc_ins.public:
            raise ORMExc.ORMException("form's currently private")

        return super().patch_rsc_ins(rsc_ins, req_body)

    def delete_rsc_ins(self, rsc_ins):
        if rsc_ins.public or rsc_ins.obsolete:
            raise ORMExc.IndelibleResourceInstance()
        return super().delete_rsc_ins(rsc_ins)
