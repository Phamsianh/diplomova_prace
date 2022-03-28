from typing import Union, Optional

from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class GroupController(BaseController):
    related_resource = [
        "positions",
        "subordinate_groups",
        "roles",
        "joiners"
    ]

    def get_resource_collection(self):
        """Get all groups in the system."""
        return super(GroupController, self).get_resource_collection()

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get a group by id."""
        return super(GroupController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """Create a group.

Constraint:

* Only admin can create group.
"""
        return super(GroupController, self).post_resource_collection(req_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update a group.

Constraint:

* Only creator of the group can update the group
"""
        if "superior_group_id" in req_body and req_body["superior_group_id"] == 0:
            req_body["superior_group_id"] = None
        return super(GroupController, self).patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """Delete a group.

        Constraint:
        * Authenticated user must be the creator of this group.
        * Group has no joiners.
        """
        if rsc_ins.joiners:
            raise ORMExc.IndelibleResourceInstance
        else:
            super().delete_resource_instance(rsc_ins)

    def get_groups_positions(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all positions in the group."""
        return super(GroupController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_groups_subordinate_groups(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all subordinate the group below 1 level."""
        return super(GroupController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_groups_roles(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all the roles in the group."""
        return super(GroupController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_groups_joiners(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all users, who joined the group."""
        return super(GroupController, self).get_related_resource(rsc_id, rel_rsc, query)

