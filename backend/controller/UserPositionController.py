from typing import Union, Optional

from controller.BaseController import BaseController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class UserPositionController(BaseController):
    related_resource = []

    def get_resource_collection(self, limit: Optional[int] = 50, offset: Optional[int] = 0, attribute: Optional[str] = None, value: Optional[str] = None, order: Optional[list] = None):
        """Get all user positions in the system."""
        return super(UserPositionController, self).get_resource_collection(limit, offset, attribute, value, order)

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get a user positions by id."""
        return super(UserPositionController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """Assign a position to another user (create users_positions record):

Constraint:

* Only admin can assign this position for other user.
"""
        val_body = self.get_val_dat(req_body, 'post')

        assigned_position = self.session.query(Model.Position).get(val_body['position_id'])
        if not assigned_position:
            raise ORMExc.ResourceInstanceNotFound(Model.Position, val_body['position_id'])
        if assigned_position.creator != self.current_user:
            raise ORMExc.RequireOwnership
        assigned_user = self.session.query(Model.User).get(val_body['user_id'])
        if not assigned_user:
            raise ORMExc.ResourceInstanceNotFound(Model.User, val_body['user_id'])

        return super(UserPositionController, self).post_resource_collection(req_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update a position to another user or update user for another position:

Constraint:

* Only admin can update this user position.
"""
        val_body = self.get_val_dat(req_body, 'patch')

        assigned_position = self.session.query(Model.Position).get(val_body['position_id'])
        if not assigned_position:
            raise ORMExc.ResourceInstanceNotFound(Model.Position, val_body['position_id'])
        if assigned_position.creator != self.current_user:
            raise ORMExc.RequireOwnership
        assigned_user = self.session.query(Model.User).get(val_body['user_id'])
        if not assigned_user:
            raise ORMExc.ResourceInstanceNotFound(Model.User, val_body['user_id'])

        return super(UserPositionController, self).patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """Delete a position from user.

        Constraint:

        * Only admin can delete a position from user.
        """
        return super(UserPositionController, self).delete_resource_instance(rsc_ins)
