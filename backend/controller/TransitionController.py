from typing import Union, Optional

from ORM.Model import Phase, Transition
from controller.FormComponentController import FormComponentController
from exceptions import ORMExceptions as ORMExc


class TransitionController(FormComponentController):
    related_resource = [
        "from_phase",
        "to_phase",
        "creator",
        "form"
    ]

    def get_resource_collection(self, limit: Optional[int] = 50, offset: Optional[int] = 0, attribute: Optional[str] = None, value: Optional[str] = None, order: Optional[list] = None):
        """Get all transitions in the system."""
        return super(TransitionController, self).get_resource_collection(limit, offset, attribute, value, order)

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get a transition by id or name."""
        return super(TransitionController, self).get_resource_instance(rsc_id)

    def post_resource_collection(self, req_body):
        """ Create a transition.

Constraint:

* 2 phases must not be the same.
* Current user must own these 2 phases.
* 2 phases must belong to 1 form.
* Form must not be public or obsolete.
* No transition existed between these 2 phases. Only 1 transition can exist between these 2 phases.
"""
        val_body = self.get_val_dat(req_body, 'post')

        if val_body['from_phase_id'] == val_body['to_phase_id']:
            raise ORMExc.ORMException("from phase and to phase must not be the same")

        from_phase = self.session.query(Phase).get(val_body['from_phase_id'])
        if not from_phase:
            raise ORMExc.ResourceInstanceNotFound(Phase, val_body['from_phase_id'])
        if from_phase.creator != self.current_user:
            raise ORMExc.RequireOwnership

        to_phase = self.session.query(Phase).get(val_body['to_phase_id'])
        if not to_phase:
            raise ORMExc.ResourceInstanceNotFound(Phase, val_body['to_phase_id'])
        if from_phase.creator != self.current_user:
            raise ORMExc.RequireOwnership

        if from_phase.form != to_phase.form:
            raise ORMExc.ORMException("from phase and to phase must belong to one form")

        if from_phase.form.public:
            raise ORMExc.ORMException('Form is public')
        if from_phase.form.obsolete:
            raise ORMExc.ORMException('Form is obsolete')

        existed_transition = self.session.query(Transition).\
            filter(Transition.from_phase_id == from_phase.id, Transition.to_phase_id == to_phase.id).first()
        if existed_transition:
            raise ORMExc.ORMException("transition already existed")

        return super().post_resource_collection(val_body)

    def patch_resource_instance(self, rsc_ins, req_body):
        """Update the transition.
        
Constraint:

* If form is public, can only change transition name.
* These 2 phases must not be the same.
* No transition existed between these 2 phases. Only 1 transition can exist between these 2 phases.
* Current user must own these 2 phase,
* These 2 phases must belong to 1 form
* Form must not be obsolete.
"""

        val_body = self.get_val_dat(req_body, 'patch')
        if val_body['from_phase_id'] == val_body['to_phase_id']:
            raise ORMExc.ORMException("from phase and to phase must not be the same")

        existed_transition = self.session.query(Transition). \
            filter(Transition.from_phase_id == val_body['from_phase_id'],
                   Transition.to_phase_id == val_body['to_phase_id']).first()
        if existed_transition and existed_transition != rsc_ins:
            raise ORMExc.ORMException("transition already existed")

        if rsc_ins.public:
            val_body['from_phase_id'] = rsc_ins.from_phase_id
            val_body['to_phase_id'] = rsc_ins.to_phase_id
            return super().patch_resource_instance(rsc_ins, val_body)

        if val_body['from_phase_id'] != rsc_ins.from_phase_id:
            from_phase = self.session.query(Phase).get(val_body['from_phase_id'])
            if not from_phase:
                raise ORMExc.ResourceInstanceNotFound(Phase, val_body['from_phase_id'])
            if from_phase.form != rsc_ins.form:
                raise ORMExc.ORMException("request from phase must belong to current form")

        if val_body['to_phase_id'] != rsc_ins.to_phase_id:
            to_phase = self.session.query(Phase).get(val_body['to_phase_id'])
            if not to_phase:
                raise ORMExc.ResourceInstanceNotFound(Phase, val_body['to_phase_id'])
            if to_phase.form != rsc_ins.form:
                raise ORMExc.ORMException("request to phase must belong to current form")

        return super().patch_resource_instance(rsc_ins, val_body)

    def delete_resource_instance(self, rsc_ins):
        """Delete a transition.

        Constraint:

        * Only admin can delete transition.
        * The form contains this transition must not be public or obsolete.
        """
        return super(TransitionController, self).delete_resource_instance(rsc_ins)

    def get_transitions_from_phase(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get source of this transition."""
        return super(TransitionController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_transitions_to_phase(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get the target phase of this transition."""
        return super(TransitionController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_transitions_form(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get the form, which contains this transition."""
        return super(TransitionController, self).get_related_resource(rsc_id, rel_rsc, query)

    def get_transitions_creator(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get the creator of the transition."""
        return super(TransitionController, self).get_related_resource(rsc_id, rel_rsc, query)
