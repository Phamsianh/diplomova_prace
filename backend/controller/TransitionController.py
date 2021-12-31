from controller.FormComponentController import FormComponentController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class TransitionController(FormComponentController):
    def post_rsc_ins(self, req_body):
        """
        To create transition between 2 phases:

        * These 2 phases must not be the same
        * Current user must own these 2 phases,
        * These 2 phases must belong to 1 form
        * Form must not be public or obsolete.
        """
        val_body = self.get_val_dat(req_body, 'post')

        if val_body['from_phase_id'] == val_body['to_phase_id']:
            raise ORMExc.ORMException("from phase and to phase must not be the same")

        from_phase = self.session.query(Model.Phase).get(val_body['from_phase_id'])
        if not from_phase:
            raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['from_phase_id'])
        if from_phase.creator != self.cur_usr:
            raise ORMExc.RequireOwnership

        to_phase = self.session.query(Model.Phase).get(val_body['to_phase_id'])
        if not to_phase:
            raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['to_phase_id'])
        if from_phase.creator != self.cur_usr:
            raise ORMExc.RequireOwnership

        if from_phase.form != to_phase.form:
            raise ORMExc.ORMException("from phase and to phase must belong to one form")
        # if from_phase.form.public:
        #     raise ORMExc.ORMException("Form is public")
        # if from_phase.form.obsolete:
        #     raise ORMExc.ORMException('Form is obsolete')

        return super().post_rsc_ins(val_body)

    def patch_rsc_ins(self, rsc_ins, req_body):
        """
        To update transition between 2 phases:

        * These 2 phases must not be the same
        * Current user must own these 2 phase,
        * These 2 phases must belong to 1 form
        * Form must not be public or obsolete.
        """

        val_body = self.get_val_dat(req_body, 'patch')
        if val_body['from_phase_id'] == val_body['to_phase_id']:
            raise ORMExc.ORMException("from phase and to phase must not be the same")

        from_phase = self.session.query(Model.Phase).get(val_body['from_phase_id'])
        if not from_phase:
            raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['from_phase_id'])
        if from_phase.creator != self.cur_usr:
            raise ORMExc.RequireOwnership

        to_phase = self.session.query(Model.Phase).get(val_body['to_phase_id'])
        if not to_phase:
            raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['to_phase_id'])
        if from_phase.creator != self.cur_usr:
            raise ORMExc.RequireOwnership

        if from_phase.form != to_phase.form:
            raise ORMExc.ORMException("from phase and to phase must belong to one form")
        # if from_phase.form.public:
        #     raise ORMExc.ORMException("Form is public")
        # if from_phase.form.obsolete:
        #     raise ORMExc.ORMException('Form is obsolete')

        return super().patch_rsc_ins(rsc_ins, val_body)


if __name__ == '__main__':
    from ORM.session import session
    from ORM.Model import User

    usr1 = session.query(User).get(1)
    fc1 = TransitionController(session=session, cur_usr=usr1)
    fc1.post_rsc_ins(req_body={
        'from_phase_id': 1,
        'to_phase_id': 2,
        'position_id': 1,
        'name': 'phase created from PhaseController'
    })
