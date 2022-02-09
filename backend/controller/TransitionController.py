from controller.FormComponentController import FormComponentController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class TransitionController(FormComponentController):
    def post_rsc_ins(self, req_body):
        """
        To create transition between 2 phases:

        * These 2 phases must not be the same.
        * Current user must own these 2 phases.
        * These 2 phases must belong to 1 form.
        * Form must not be public or obsolete.
        * No transition existed between these 2 phases. Only 1 transition can exist between these 2 phases.
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

        if from_phase.form.public:
            raise ORMExc.ORMException('Form is public')
        if from_phase.form.obsolete:
            raise ORMExc.ORMException('Form is obsolete')

        existed_transition = self.session.query(Model.Transition).\
            filter(Model.Transition.from_phase_id == from_phase.id, Model.Transition.to_phase_id == to_phase.id).first()
        if existed_transition:
            raise ORMExc.ORMException("transition already existed")

        return super().post_rsc_ins(val_body)

    def patch_rsc_ins(self, rsc_ins, req_body):
        """
        To update transition between 2 phases:

        * If form is public, can only change transition name
        * These 2 phases must not be the same
        * No transition existed between these 2 phases. Only 1 transition can exist between these 2 phases.
        * Current user must own these 2 phase,
        * These 2 phases must belong to 1 form
        * Form must not be obsolete.
        """

        val_body = self.get_val_dat(req_body, 'patch')
        if val_body['from_phase_id'] == val_body['to_phase_id']:
            raise ORMExc.ORMException("from phase and to phase must not be the same")

        existed_transition = self.session.query(Model.Transition). \
            filter(Model.Transition.from_phase_id == val_body['from_phase_id'],
                   Model.Transition.to_phase_id == val_body['to_phase_id']).first()
        if existed_transition and existed_transition != rsc_ins:
            raise ORMExc.ORMException("transition already existed")

        if rsc_ins.public:
            val_body['from_phase_id'] = rsc_ins.from_phase_id
            val_body['to_phase_id'] = rsc_ins.to_phase_id
            return super().patch_rsc_ins(rsc_ins, val_body)

        if val_body['from_phase_id'] != rsc_ins.from_phase_id:
            from_phase = self.session.query(Model.Phase).get(val_body['from_phase_id'])
            if not from_phase:
                raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['from_phase_id'])
            if from_phase.form != rsc_ins.form:
                raise ORMExc.ORMException("request from phase must belong to current form")

        if val_body['to_phase_id'] != rsc_ins.to_phase_id:
            to_phase = self.session.query(Model.Phase).get(val_body['to_phase_id'])
            if not to_phase:
                raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['to_phase_id'])
            if to_phase.form != rsc_ins.form:
                raise ORMExc.ORMException("request to phase must belong to current form")

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
