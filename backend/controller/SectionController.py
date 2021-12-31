from controller.FormComponentController import FormComponentController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class SectionController(FormComponentController):
    def post_rsc_ins(self, req_body):
        """To create section for a phase

        * Current user must own this phase
        * The form, which this phase belongs to, must not be public or obsolete
        * First section created for phase must be section for director.
        """
        val_body = self.get_val_dat(req_body, 'post')

        phase = self.session.query(Model.Phase).get(val_body['phase_id'])
        if not phase:
            raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['phase_id'])
        if self.cur_usr != phase.form.creator:
            raise ORMExc.RequireOwnership

        if phase.form.public:
            raise ORMExc.ORMException("Form is public")
        if phase.form.obsolete:
            raise ORMExc.ORMException("Form is obsolete")

        if not phase.sections and val_body['position_id'] != phase.position_id:
            raise ORMExc.ORMException("first section of the phase must be assigned for director")
        return super().post_rsc_ins(val_body)

    def patch_rsc_ins(self, rsc_ins, req_body):
        """
        To update section:

        *  ``phase_id``: If this section is currently designated section and
         if phase doesn't exist another designated section(s), raise error. Request phase must belong to current form.
        *  ``position_id``: If this section is currently designated section and
         if phase doesn't exist another designated section(s), raise error.
        """
        val_bod = self.get_val_dat(req_body, 'patch')
        if hasattr(val_bod, 'position_id') or hasattr(val_bod, 'phase_id'):
            if hasattr(val_bod, 'phase_id'):
                req_phase = self.session.query(Model.Phase).get(val_bod['phase_id'])
                if rsc_ins.form != req_phase.form:
                    raise ORMExc.ORMException("phase must belong to current form")

            designated_sections = rsc_ins.phase.designated_sections
            if rsc_ins in designated_sections and len(designated_sections) == 1:
                raise ORMExc.ORMException("section is currently only designated section of current phase")
        return super().patch_rsc_ins(rsc_ins, req_body)


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
