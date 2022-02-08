from controller.FormComponentController import FormComponentController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class PhaseController(FormComponentController):
    def post_rsc_ins(self, req_body):
        """To create Phase for a form

        * Current user must be form's owner
        * Form must not be public or obsolete
        """
        val_body = self.get_val_dat(req_body, 'post')

        form = self.session.query(Model.Form).get(val_body['form_id'])
        if not form:
            raise ORMExc.ResourceInstanceNotFound(Model.Form, val_body['form_id'])
        if self.cur_usr != form.creator:
            raise ORMExc.RequireOwnership
        if form.public:
            raise ORMExc.ORMException("Form is public")
        if form.obsolete:
            raise ORMExc.ORMException("Form is obsolete")

        return super().post_rsc_ins(val_body)

    def patch_rsc_ins(self, rsc_ins, req_body):
        """Phase's owner can update phase's name, description, positions_id, phase_type

        Requirements:

        * If form is public, positions_id and phase_type can not be changed
        """
        val_body = self.get_val_dat(req_body, 'patch')

        if rsc_ins.public:
            val_body['positions_id'] = rsc_ins.position_id
            val_body['phase_type'] = rsc_ins.phase_type

        return super().patch_rsc_ins(rsc_ins, val_body)


if __name__ == '__main__':
    from ORM.session import session
    from ORM.Model import User
    usr1 = session.query(User).get(1)
    fc1 = PhaseController(session=session, cur_usr=usr1)
    fc1.post_rsc_ins(req_body={
        'form_id': 1,
        'position_id': 1,
        'name': 'phase created from PhaseController'
    })
