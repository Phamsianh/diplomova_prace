from typing import Union
from controller.FormComponentController import FormComponentController
from ORM import Model
from exceptions import ORMExceptions as ORMExc


class SectionController(FormComponentController):
    related_resource = [
        "creator",
        "form",
        "phase",
        "position",
        "fields",
        "potential_handlers",
        "potential_receivers",
    ]

    def get_resource_collection(self):
        """Get all sections in the system."""
        return super().get_resource_collection()

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get a section by id."""
        return super().get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """To create section for a phase

* Current user must be phase's owner.
* The form, which this phase belongs to, must not be public or obsolete.
        """
        val_body = self.get_val_dat(req_body, 'post')

        phase = self.session.query(Model.Phase).get(val_body['phase_id'])
        if not phase:
            raise ORMExc.ResourceInstanceNotFound(Model.Phase, val_body['phase_id'])
        if self.current_user != phase.creator:
            raise ORMExc.RequireOwnership
        if phase.public:
            raise ORMExc.ORMException("Form is public")
        if phase.obsolete:
            raise ORMExc.ORMException("Form is obsolete")

        return super().post_resource_collection(val_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Constraint when update a section:

* Current user must be phase's owner.
* ``name``, ``phase_id`` and ``position_id`` can only be changed when form is currently private.
* ``phase_id`` must belong to the same form as the old phase id.
        """
        val_bod = self.get_val_dat(req_body, 'patch')

        if rsc_ins.public or rsc_ins.obsolete:
            if 'name' in val_bod:
                val_bod['name'] = rsc_ins.name
            if 'positions_id' in val_bod:
                val_bod['position_id'] = rsc_ins.position_id
            if 'phase_id' in val_bod:
                val_bod['phase_id'] = rsc_ins.phase_id
        else:
            if 'phase_id' in val_bod:
                req_phase = self.session.query(Model.Phase).get(val_bod['phase_id'])
                if rsc_ins.form != req_phase.form:
                    raise ORMExc.ORMException("requested new phase must belong to the same form as the old phase")

        return super().patch_resource_instance(rsc_ins, val_bod)

    def get_sections_creator(self, rsc_id, rel_rsc, query):
        """Get creator of the section, eventually the form."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_sections_form(self, rsc_id, rel_rsc, query):
        """Get the form, which contains the section."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_sections_phase(self, rsc_id, rel_rsc, query):
        """Get the phase, which contains the section."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_sections_position(self, rsc_id, rel_rsc, query):
        """Get the position assigned for the section."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_sections_fields(self, rsc_id, rel_rsc, query):
        """Get all fields contained in the section."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_sections_potential_handlers(self, rsc_id, rel_rsc, query):
        """Get all potential handlers of the section.
        Potential handlers of a section is users, who have positions, which is assigned for handling this section."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_sections_potential_receivers(self, rsc_id, rel_rsc, query):
        """Get all potential receivers of the section.
        Potential receivers of a section is users, who have positions, which is assigned for handling this section."""
        return self.get_related_resource(rsc_id, rel_rsc, query)
