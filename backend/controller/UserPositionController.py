from controller.BaseController import BaseController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class UserPositionController(BaseController):
    def post_rsc_ins(self, req_body):
        """
        To assign a position to another user (create users_positions record):

        * Current user must have own this position.
        """
        val_body = self.get_val_dat(req_body, 'post')

        assigned_pst = self.session.query(Model.Position).get(val_body['position_id'])
        if not assigned_pst:
            raise ORMExc.ResourceInstanceNotFound(Model.Position, val_body['position_id'])
        if assigned_pst.creator != self.cur_usr:
            raise ORMExc.RequireOwnership
        assigned_usr = self.session.query(Model.User).get(val_body['user_id'])
        if not assigned_usr:
            raise ORMExc.ResourceInstanceNotFound(Model.User, val_body['user_id'])

        super().post_rsc_ins(val_body)


if __name__ == '__main__':
    from ORM.session import session
    from ORM.Model import User

    usr1 = session.query(User).get(1)
    fc1 = UserPositionController(session=session, cur_usr=usr1)
    fc1.post_rsc_ins(req_body={
        'user_id': 1,
        'positio_id': 10
    })
