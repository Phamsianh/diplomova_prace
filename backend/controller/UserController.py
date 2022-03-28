from typing import Union

from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class UserController(BaseController):
    related_resource = [
        "users_positions",
        "created_forms",
        "created_instances",
        "directors",
        "receivers",
        "held_positions",
        "joined_group",
        "held_roles",
        "participated_instances",
        "pending_instances",
        "potential_instances",
    ]

    def get_resource_collection(self):
        """Get all users of the system, default number of users return is 50."""
        return super(UserController, self).get_resource_collection()

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get the user instance."""
        if rsc_id == 'me':
            rsc_ins = self.current_user
        elif type(rsc_id) == str:
            rsc_ins = self.session.query(self.model).filter(self.model.user_name == rsc_id).first()
        else:
            rsc_ins = super().get_resource_instance(rsc_id)
        if rsc_ins is None:
            raise ORMExc.ResourceInstanceNotFound(self.model, rsc_id)
        else:
            return rsc_ins

    def post_resource_collection(self, req_body):
        """Create a user."""
        return super().post_resource_collection(req_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update a user."""
        return super().patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """User resource cannot be deleted."""
        raise ORMExc.IndelibleResourceInstance

    def get_users_users_positions(self, rsc_id, rel_rsc, query):
        """Get all users_positions of authenticated user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_created_forms(self, rsc_id, rel_rsc, query):
        """Get all forms created by the authenticated user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_created_instances(self, rsc_id, rel_rsc, query):
        """Get all instances created by the authenticated user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_directors(self, rsc_id, rel_rsc, query):
        """Get all directors specified for the authenticated user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_receivers(self, rsc_id, rel_rsc, query):
        """Get all receivers specified for the authenticated user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_held_positions(self, rsc_id, rel_rsc, query):
        """Get all positions held by the user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_joined_groups(self, rsc_id, rel_rsc, query):
        """Get all groups joined by the user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_held_roles(self, rsc_id, rel_rsc, query):
        """Get all  positions held by the user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_participated_instances(self, rsc_id, rel_rsc, query):
        """Get all instances participated by the user."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_pending_instances(self, rsc_id, rel_rsc, query):
        """Get all instances, which are pending for the user to receive or to redirect."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)

    def get_users_potential_instances(self, rsc_id, rel_rsc, query):
        """Get all instances, which are potential for the user to receive or to redirect."""
        return self.get_related_resource(rsc_id=rsc_id, rel_rsc=rel_rsc, query=query)
