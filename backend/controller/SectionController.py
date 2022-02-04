from controller.FormComponentController import FormComponentController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class SectionController(FormComponentController):
    def post_rsc_ins(self, req_body):
        """To create section for a phase

        * Current user must be phase's owner
        * The form, which this phase belongs to, must not be obsolete
        """
        val_body = self.get_val_dat(req_body, 'post')

        phase = self.session.query(Model.Phase).get(val_body['phase_id'])
        if not phase:
            raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['phase_id'])
        if self.cur_usr != phase.creator:
            raise ORMExc.RequireOwnership
        if phase.obsolete:
            raise ORMExc.ORMException("Form is obsolete")

        return super().post_rsc_ins(val_body)

    def patch_rsc_ins(self, rsc_ins, req_body):
        """
        Form's owner can update section's name, phase_id, position_id, order

        Requirement:
        * Request phase_id must belong to current form
        * If form is public, position_id can not be changed
        """
        val_bod = self.get_val_dat(req_body, 'patch')

        if hasattr(val_bod, 'phase_id'):
            req_phase = self.session.query(Model.Phase).get(val_bod['phase_id'])
            if rsc_ins.form != req_phase.form:
                raise ORMExc.ORMException("request phase must belong to current form")

        if rsc_ins.public:
            val_bod['position_id'] = rsc_ins.position_id

        return super().patch_rsc_ins(rsc_ins, val_bod)


if __name__ == '__main__':
    from ORM.session import session
    from ORM.Model import User

    usr1 = session.query(User).get(1)
    fc1 = SectionController(session=session, cur_usr=usr1)
    fc1.post_rsc_ins(req_body={
        'from_phase_id': 1,
        'to_phase_id': 2,
        'position_id': 1,
        'name': 'phase created from PhaseController'
    })
