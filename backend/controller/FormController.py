from typing import Union

from controller.BaseController import BaseController
from exceptions import ORMExceptions as ORMExc


class FormController(BaseController):
    related_resource = [
        "creator",
        "phases",
        "transitions",
        "sections",
        "fields",
        "instances",
        "positions",
        "available_positions"
    ]

    def get_resource_collection(self):
        """Get all the public forms in the system."""
        from ORM.Model import Form
        public_forms = self.session.query(Form).filter(Form.public == True).limit(50).all()
        return public_forms

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get form from id."""
        return super(FormController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """Create a form.
        The form created doesn't have any form component, e.g. phase, transition, section or field.
        To create these component please refer to the Post Resource Collection endpoint type of correspond resource.
        """
        return super(FormController, self).post_resource_collection(req_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Constraint when public a form:

* Only 1 begin phase and 1 end phase.
* Each phase must at least has 1 section, each section must at least has 1 field.

*Note: public form cannot change to private.*

Constraint when deprecate a form:

* Form must be public.

*Note: obsolete form cannot change to be not obsolete.*
        """
        if rsc_ins.obsolete:
            raise ORMExc.ORMException("form is obsolete, cannot be changed")

        if 'name' in req_body and rsc_ins.public:
            raise ORMExc.ORMException("name of public form cannot be changed")

        if 'public' in req_body:
            if req_body['public'] and not rsc_ins.public:
                if len(rsc_ins.begin_phases) != 1 or len(rsc_ins.end_phases) != 1:
                    raise ORMExc.ORMException("form must have 1 begin phase and 1 end phase")
                for p in rsc_ins.phases:
                    for s in p.sections:
                        if not s.fields:
                            raise ORMExc.ORMException("Each phase must at least has 1 section,"
                                                      " and each section must at least has 1 field.")
            if not req_body['public'] and rsc_ins.public:
                raise ORMExc.ORMException("form is public, cannot change to private")

        if 'obsolete' in req_body and req_body['obsolete'] and not rsc_ins.public:
            raise ORMExc.ORMException("form's currently private")

        return super().patch_resource_instance(rsc_ins, req_body)

    def delete_resource_instance(self, rsc_ins):
        """The form can only be deleted if it is private."""
        if rsc_ins.public or rsc_ins.obsolete:
            raise ORMExc.IndelibleResourceInstance()
        return super().delete_resource_instance(rsc_ins)

    def get_forms_creator(self, rsc_id, rel_rsc, query):
        """Get creator of the form."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_forms_phases(self, rsc_id, rel_rsc, query):
        """Get all phases of the form."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_forms_transitions(self, rsc_id, rel_rsc, query):
        """Get all transitions of the form."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_forms_sections(self, rsc_id, rel_rsc, query):
        """Get all sections of the form."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_forms_fields(self, rsc_id, rel_rsc, query):
        """Get all fields of the form."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_forms_instances(self, rsc_id, rel_rsc, query):
        """Get all instances instantiated from the form.

        Constraint:

        * Only admin can get the information of all instances, which are instantiated from this form."""
        if not self.current_user.is_admin:
            raise ORMExc.ORMException("you are not admin. only admin can use this endpoint")
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_forms_positions(self, rsc_id, rel_rsc, query):
        """Get all positions, either designated for a phases or assigned for handle sections of the form."""
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_forms_available_positions(self, rsc_id, rel_rsc, query):
        """Get all positions, either designated for a phases or assigned for handling sections of the form.
         This endpoint is an alias for Get Forms Positions endpoint."""
        return self.get_related_resource(rsc_id, rel_rsc, query)
