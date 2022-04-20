from typing import Union, Optional
from ORM.Model import Instance, Section, UserPosition, Receiver
from exceptions.ORMExceptions import ORMException
from controller.BaseController import BaseController


class ReceiverController(BaseController):
    related_resource = []

    def get_resource_collection(self, limit: Optional[int] = 50, offset: Optional[int] = 0, attribute: Optional[str] = None, value: Optional[str] = None, order: Optional[list] = None):
        """Get all receivers in the system.
        
        Constraint:
        * Only admin can get all receivers in the system"""
        if self.current_user.is_admin:
            raise ORMException("you are not an admin")
        return super().get_resource_collection(limit, offset, attribute, value, order)

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get the receiver by id.
        
        Constraint:
        * Only participants of the instance can get the receiver."""

        rsc_ins = super().get_resource_instance(rsc_id)
        if self.current_user not in rsc_ins.instance.participants:
            raise ORMException("you are not a participants of the instance")
        return rsc_ins

    def post_resource_collection(self, req_body):
        """Create a receiver for an instance.

Constraint:
* Only director of the instance can add another receiver to the instance.
* Section must belong the the section.
* The specified receiver must not preexist.
* Specified user must be a potential handler for the instance.
"""
        val_bod = self.get_val_dat(req_body, 'post')

        instance: Instance = self.session.query(Instance).get(val_bod["instance_id"])
        if not instance:
            raise ORMException("instance not found")
        if self.current_user != instance.current_director_user:
            raise ORMException("you are not current director of this instance")

        section = self.session.query(Section).get(val_bod["section_id"])
        if not section:
            raise ORMException("section not found")
        if section not in instance.current_sections:
            raise ORMException("section not belong to instance")

        existed_receiver = self.session.query(Receiver).filter(
            Receiver.instance_id == instance.id, 
            Receiver.section_id == section.id).first()
        if existed_receiver:
            raise ORMException("receiver for section already existed")

        user_have_assigned_position = self.session.query(UserPosition).filter(
            UserPosition.user_id == val_bod["user_id"],
            UserPosition.position_id == section.position_id
            ).first()
        if not user_have_assigned_position:
            raise ORMException("user is not found or user does not have assigned position")
        return super().post_resource_collection(req_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update the receiver.

Constraint:
* Only director of current phase of the instance can update the receiver(s) of current sections of the instance.
* Specified user must be a potential handler for the instance.
"""
        val_bod = self.get_val_dat(req_body, 'patch')

        if self.current_user != rsc_ins.instance.current_director_user:
            raise ORMException("you are not current director of this instance")

        user_have_assigned_position = self.session.query(UserPosition).filter(
            UserPosition.user_id == val_bod["user_id"],
            UserPosition.position_id == rsc_ins.section.position_id
            ).first()
        if not user_have_assigned_position:
            raise ORMException("user is not found or user does not have assigned position")

        return super().patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """Receiver cannot be deleted."""
        raise ORMException("Resource indelible")