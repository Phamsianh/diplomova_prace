from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc
from ORM.Model import InstanceField, Receiver, Section, Field


class InstanceFieldController(BaseController):
    def post_rsc_ins(self, req_body):
        raise ORMExc.ORMException("resource can not be created manually")

    def patch_rsc_ins(self, rsc_ins, req_body):
        if self.cur_usr not in rsc_ins.instance.current_receivers_users:
            raise ORMExc.ORMException("you're not a current receiver of this phase")

        query = self.session.query(Receiver.user_id).join(Receiver.section).join(Section.fields).\
            join(Field.instances_fields).\
            filter(InstanceField.id == rsc_ins.id).all()
        receivers_users_id = list(zip(*query))[0]
        if self.cur_usr.id not in receivers_users_id:
            raise ORMExc.ORMException("you're not receiver of this instance field")

        return super().patch_rsc_ins(rsc_ins, req_body)

    def delete_rsc_ins(self, rsc_ins):
        raise ORMExc.IndelibleResourceInstance()

# Instance field cannot be updated by participants if they are not receivers of current phase

