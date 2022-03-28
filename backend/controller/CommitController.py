from typing import Union, Optional

from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class CommitController(BaseController):
    related_resource = [
        "instance",
        "prev_commit",
        "envelopes",
    ]

    def get_resource_collection(self):
        """Get all commits in the system

        Constraint:

        * Only admin can retrieve all commits in the system.
        """
        return super(CommitController, self).get_resource_collection()

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get commit by hash.

        Constraint:

        * Only participants of the instance can retrieve the commit.
        """
        rsc_ins = self.session.query(self.model).get(rsc_id)
        if not rsc_ins:
            raise ORMExc.ResourceInstanceNotFound(self.model, rsc_id)
        if self.current_user not in rsc_ins.instance.participants:
            raise ORMExc.ORMException("you are not a participant of this instance")
        return rsc_ins

    def post_resource_collection(self, req_body):
        """Commit cannot be created create manually.
        It's created when user transit instance to next phase.
        Please refer to endpoint Patch Instances Resource Instance.
        """
        raise ORMExc.ORMException("Commit cannot be created manually."
                                  " It's created when user transit instance to next phase."
                                  "Please refer to the endpoint Patch Instances Resource Instance.")

    def patch_resource_instance(self, rsc_ins, req_body):
        """Commit cannot be modified cause a history cannot be modified."""
        raise ORMExc.ORMException("Commit cannot be modified.")

    def delete_resource_instance(self, rsc_ins):
        """Commit cannot be deleted."""
        raise ORMExc.IndelibleResourceInstance

    def get_commits_instance(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get the instance, which the commit belongs to.

        Constraint:

        * Only participants of the instance can get this resource."""
        return super(CommitController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_commits_prev_commit(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get the previous commit of the current commit.

        Constraint:

        * Only participants of the instance can get this resource."""
        return super(CommitController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_commits_envelopes(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all evelopes of the commit.

        Constraint:

        * Only participants of the instance can get this resource.
        """
        return super(CommitController, self).get_related_resource(rsc_id, rel_rsc, query)
