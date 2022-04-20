from typing import Union, Optional

from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class PositionController(BaseController):
    related_resource = [
        # "phases",
        "users_positions",
        # "sections",
        "holders",
    ]

    def get_resource_collection(self, limit: Optional[int] = 50, offset: Optional[int] = 0, attribute: Optional[str] = None, value: Optional[str] = None, order: Optional[list] = None):
        """Get all positions in the system."""
        return super(PositionController, self).get_resource_collection(limit, offset, attribute, value, order)

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get position by id."""
        return super(PositionController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """Create a position.

Constraint:

* Only admin can create a position.
"""
        return super(PositionController, self).post_resource_collection(req_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update a position.

Constraint:

* Only creator can update the position.
"""
        return super(PositionController, self).patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """Delete a position.
        Constraint:
        * Only creator can delete the position
        * There must not be any user, who is holding this position."""
        if rsc_ins.holders:
            raise ORMExc.IndelibleResourceInstance
        else:
            super().delete_resource_instance(rsc_ins)

    def get_positions_users_positions(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all users positions of this position."""
        return super(PositionController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_positions_holders(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all users, who are holding this position."""
        return super(PositionController, self).get_related_resource(rsc_id, rel_rsc, query)
