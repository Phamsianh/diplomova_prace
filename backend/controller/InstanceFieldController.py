from typing import Union, Optional

from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc
from ORM.Model import InstanceField, Receiver, Section, Field


class InstanceFieldController(BaseController):
    related_resource = [
        "receiver"
    ]

    def get_resource_collection(self, limit: Optional[int] = 50, offset: Optional[int] = 0, attribute: Optional[str] = None, value: Optional[str] = None, order: Optional[list] = None):
        """Contents can only be retrieved through endpoint Get Instances Instances Fields.

        For development process, this constraint is disable.
        """
        return super(InstanceFieldController, self).get_resource_collection(limit, offset, attribute, value, order)
        # raise ORMExc.ORMException("contents can only be retrieved through endpoint Get Instances Instances Fields")

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get the content of the instance.

        Constraint:

        * Content can only be retrieved by participant of the instance."""
        content = self.session.query(InstanceField).get(rsc_id)
        if self.current_user not in content.instance.participants:
            raise ORMExc.ORMException("you are not a participant of the instance")
        return super(InstanceFieldController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """
The content (instance field) cannot be created manually.
The content is auto created when handler receives the instance.
Please refer to the endpoint Patch Instances Resource Instance.
"""
        raise ORMExc.ORMException("resource can not be created manually")

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update content.  
        
Constraint:

* The current authenticated user must be the receiver of the content.
"""
        if self.current_user != rsc_ins.receiver:
            raise ORMExc.ORMException("you're not receiver of this instance field")

        # update creator of the content in case the receiver of the instance can be changed by the director.
        # this creator_id of the content is used for creating the envelope. Refer to Commiter.create_envelope() method.
        rsc_ins.creator_id = self.current_user.id
        return super().patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """Content once were created, cannot be deleted."""
        raise ORMExc.IndelibleResourceInstance()

    def get_instances_fields_receiver(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get receiver of this content.

        Constraint:

        * Only participant of this instance can use this endpoint."""
        return super(InstanceFieldController, self).get_related_resource(rsc_id, rel_rsc, query)
