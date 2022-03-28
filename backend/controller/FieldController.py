from typing import Union

from controller.FormComponentController import FormComponentController
from ORM.Model import Section, Phase
from exceptions import ORMExceptions as ORMExc


class FieldController(FormComponentController):
    related_resource = []

    def get_resource_collection(self):
        """Get all fields in the system."""
        return super(FieldController, self).get_resource_collection()

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get the field by id."""
        return super(FieldController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """Create a field.

Constraint:

* Current user must be section's owner.
* The form, which this section belongs to, must not be public or obsolete.
        """
        val_body = self.get_val_dat(req_body, 'post')

        section = self.session.query(Section).get(val_body['section_id'])
        if not section:
            raise ORMExc.ResourceInstanceNotFound(Phase, val_body['section_id'])
        if self.current_user != section.creator:
            raise ORMExc.RequireOwnership
        if section.public:
            raise ORMExc.ORMException("Form is public")
        if section.obsolete:
            raise ORMExc.ORMException("Form is obsolete")

        return super().post_resource_collection(val_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update the field.

Constraint:

* Current user must be section's owner.
* ``name`` and ``section_id`` can only be updated when the form, which contains this field is private.
* ``section_id`` must belong to the same form as the old section id.
"""
        val_bod = self.get_val_dat(req_body, 'patch')

        if rsc_ins.public or rsc_ins.obsolete:
            if 'name' in val_bod:
                val_bod['name'] = rsc_ins.name
            if 'section_id' in val_bod:
                val_bod['section_id'] = rsc_ins.section_id
        else:
            if 'section_id' in val_bod:
                req_section = self.session.query(Section).get(val_bod['section_id'])
                if req_section.form != rsc_ins.form:
                    raise ORMExc.ORMException("section_id must belong to the same form as the old section_id")

        return super(FieldController, self).patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """Delete a field.

        Constraint:

        * Only creator of the field can delete this field.
        * Field of public or obsolete form cannot be deleted."""
        return super(FieldController, self).delete_resource_instance(rsc_ins)
