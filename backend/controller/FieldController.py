from controller.FormComponentController import FormComponentController
from ORM.Model import Section, Phase
from exceptions import ORMExceptions as ORMExc


class FieldController(FormComponentController):
    def post_rsc_ins(self, req_body):
        val_body = self.get_val_dat(req_body, 'post')

        section = self.session.query(Section).get(val_body['section_id'])
        if not section:
            raise ORMExc.ResourceInstanceNotFound(Phase, val_body['section_id'])
        form = section.form
        if self.cur_usr != form.creator:
            raise ORMExc.RequireOwnership
        if form.public:
            raise ORMExc.ORMException("Form is public")
        if form.obsolete:
            raise ORMExc.ORMException("Form is obsolete")

        return super().post_rsc_ins(val_body)


if __name__ == '__main__':
    from ORM.session import session
    from ORM.Model import User
    usr1 = session.query(User).get(1)
    fc1 = FieldController(session=session, cur_usr=usr1)
    fc1.post_rsc_ins(req_body={
        'name': 'field created from FieldController',
        'section_id': 1,
        'abc': 'bca'
    })