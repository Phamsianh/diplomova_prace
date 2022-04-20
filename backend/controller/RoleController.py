from typing import Union, Optional

from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class RoleController(BaseController):
    related_resource = [
        "positions",
        "groups",
        "holders",
    ]

    def get_resource_collection(self, limit: Optional[int] = 50, offset: Optional[int] = 0, attribute: Optional[str] = None, value: Optional[str] = None, order: Optional[list] = None):
        """Get all roles defined in the system."""
        return super(RoleController, self).get_resource_collection(limit, offset, attribute, value, order)

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get role by id."""
        return super(RoleController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """Create a role.

Constraint:

* Only admin can create a role.
"""
        return super(RoleController, self).post_resource_collection(req_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update the role.

Constraint:

* Only creator of the role can update it.
"""
        return super(RoleController, self).patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """Delete a role.
        
        Constraint:
        * Only owner of the role can delete it.
        * The role without any holders can be delete.
        """
        if rsc_ins.holders:
            raise ORMExc.IndelibleResourceInstance
        else:
            super().delete_resource_instance(rsc_ins)

    def get_roles_positions(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all positions, which are derived from this role."""
        return super(RoleController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_roles_groups(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all groups, which have this role."""
        return super(RoleController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_roles_holders(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all user, who held this role."""
        return super(RoleController, self).get_related_resource(rsc_id, rel_rsc, query)
