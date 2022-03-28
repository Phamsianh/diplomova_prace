from typing import Union, Optional

from controller.FormComponentController import FormComponentController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class PhaseController(FormComponentController):
    related_resource = [
        "sections",
        "fields",
        "from_transitions",
        "to_transitions",
        "next_phases",
        "prev_phases",
        "potential_directors"
    ]

    def get_resource_collection(self):
        """Get all phases of all forms in the system."""
        return super(PhaseController, self).get_resource_collection()

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get a phase by id."""
        return super(PhaseController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """Create a phase for a form.

Constraint when create a phase:

* Current user must be form's owner.
* Form must not be public or obsolete.
"""
        val_body = self.get_val_dat(req_body, 'post')

        form = self.session.query(Model.Form).get(val_body['form_id'])
        if not form:
            raise ORMExc.ResourceInstanceNotFound(Model.Form, val_body['form_id'])
        if self.current_user != form.creator:
            raise ORMExc.RequireOwnership
        if form.public:
            raise ORMExc.ORMException("Form is public")
        if form.obsolete:
            raise ORMExc.ORMException("Form is obsolete")

        return super().post_resource_collection(val_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update the phase.

Constraint:

* If form is public, positions_id and phase_type can not be changed.
"""
        val_body = self.get_val_dat(req_body, 'patch')

        if rsc_ins.public:
            val_body['positions_id'] = rsc_ins.position_id
            val_body['phase_type'] = rsc_ins.phase_type

        return super().patch_resource_instance(rsc_ins, val_body)

    def delete_resource_instance(self, rsc_ins):
        """Delete a phase.

        Constraint:

        * Only admin can delete a phase.
        * Only phase of private form can be delete. Phases of public or obsolete form cannot be deleted."""
        return super(PhaseController, self).delete_resource_instance(rsc_ins)

    def get_phases_sections(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all section of the phase."""
        return super(PhaseController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_phases_fields(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all fields of the phase."""
        return super(PhaseController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_phases_from_transitions(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all transitions, whose source is this phase."""
        return super(PhaseController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_phases_to_transitions(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all transitions, whose target is this phase."""
        return super(PhaseController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_phases_next_phases(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all next phases of this phase."""
        return super(PhaseController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_phases_prev_phases(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all previous phases of this phase."""
        return super(PhaseController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_phases_potential_directors(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all users, which have positions designated for this phase."""
        return super(PhaseController, self).get_related_resource(rsc_id, rel_rsc, query)

