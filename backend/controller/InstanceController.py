from typing import Optional, List
from ORM.session import session
from controller.BaseController import BaseController
from ORM.Model import Form, InstanceField, Instance, Phase
from exceptions import ORMExceptions as ORMExc
from exceptions import InstanceException as InsExc


class InstanceController(BaseController):
    def post_rsc_ins(self, req_body):
        """
        To create (initialize) instance from a form, the form must not be public or obsolete.
        Instance initialization includes:

        * Set the current phase of this instance to begin phase of the form if user have assigned position.
        * Create all begin fields with value is null.
        """
        val_body = self.get_val_dat(req_body, 'post')

        # check if form is public and obsolete
        form = self.session.query(Form).filter(Form.public == True, Form.id == val_body['form_id']).first()
        if not form:
            raise ORMExc.ResourceInstanceNotFound(Form, val_body['form_id'])
        if form.obsolete:
            raise InsExc.InstanceException("Form is obsolete")

        # check if user have assigned position for begin phase of the form and set current phase of this instance to
        # begin phase of the form
        begin_phase = form.begin_phase
        if begin_phase.position not in self.cur_usr.held_positions:
            raise InsExc.InstanceException("You can not init this form")
        new_ins = self.model(**val_body)
        new_ins.current_phase_id = begin_phase.id

        # create all begin fields for this instance
        begin_fields = form.begin_fields
        for begin_field in begin_fields:
            new_ins.instances_fields.append(InstanceField(
                field_id=begin_field.id,
                creator_id=self.cur_usr.id
            ))
        new_ins.creator_id = self.cur_usr.id
        try:
            self.session.add(new_ins)
            self.session.flush()
        except:
            raise
        else:
            self.session.commit()
            self.session.refresh(new_ins)
        return new_ins

    def patch_rsc_ins(self, rsc_ins, req_body):
        """
        Update instance include:
        Transit instance from 1 phase to next phase or/and handle instance
        * ``rsc_id``: resource id
        * ``req_body``: request body data
        """
        val_body = self.get_val_dat(req_body, 'patch')

        if "current_phase_id" in val_body:
            self.transit_instance(val_body["current_phase_id"], rsc_ins)
        if "instance_handle_request" in val_body and val_body["instance_handle_request"]["handle"]:
            self.handle_instance(
                rsc_ins,
                val_body["instance_handle_request"]["handled_positions_id"]
                if "handled_positions_id" in val_body["instance_handle_request"]
                else None)
        self.session.commit()
        self.session.refresh(rsc_ins)
        return rsc_ins

    def transit_instance(self, nxt_phs_id: int, ins: Instance):
        """
        To transit instance:

        * Current user must held designated position
        * Instance must have state 'full resolved'
        * Requested next phase must be 1 of available next phases
        """
        if ins.current_designated_position not in self.cur_usr.held_positions:
            raise InsExc.InstanceException("you're not director of this phase")
        else:
            ins_cur_state = ins.current_state
            if ins_cur_state != "full resolved":
                raise InsExc.CurrentPhaseNotResolved(ins_cur_state)
            else:
                req_next_phase = self.session.query(Phase).get(nxt_phs_id)
                avai_next_phases = ins.current_phase.next_phases
                if req_next_phase not in avai_next_phases:
                    raise InsExc.NotAvailableNextPhases(nxt_phs_id, ins.id, avai_next_phases)
                else:
                    from ORM.Commiter import Committer
                    committer = Committer(self.session, self.cur_usr, ins)
                    committer.commit()
                    ins.current_phase_id = req_next_phase.id

    def handle_instance(self, ins: Instance, hdl_psts_id: Optional[List[int]]):
        """
        To handle instance, current user can specify with which position(s) (s)he handles the instance.
        If handle positions is not specified, current user will handle all available part with all available positions,
        which (s)he holds.

        Handle instance include:
        1. initialize specified or all parts
        2. exchange key from instance's creator and handler. Thus handler can create envelopes to commit.
        """
        if ins.current_state not in ["pending", "partial received", "partial received & partial resolved"]:
            raise InsExc.CurrentlyNotRequireHandle
        if self.cur_usr not in ins.current_potential_handlers:
            raise ORMExc.ORMException("you're not potential handlers of this instance")
        if hdl_psts_id:
            self.check_requested_positions(hdl_psts_id, ins)
            val_req_psts_id = hdl_psts_id
        else:
            val_req_psts_id = [pst.id for pst in ins.current_remaining_positions if pst in self.cur_usr.held_positions]
        for p_id in val_req_psts_id:
            self.init_part(ins, p_id)

    def check_requested_positions(self, req_psts_id: List[int], ins: Instance):
        """
        User must holds all requested positions and all requested positions must be remaining positions.

        * ``req_psts_id``: positions, which user requests to handle specific parts of current phase.\n
        * ``ins``: instance, which is requested to be handle by user.\n
        """
        usr_psts_id = [pst.id for pst in self.cur_usr.held_positions]
        cur_rmn_psts_id = [pst.id for pst in ins.current_remaining_positions]
        for p_id in req_psts_id:
            if p_id not in usr_psts_id:
                raise ORMExc.ORMException(f"you're don't have position {p_id}")
            if p_id not in cur_rmn_psts_id:
                raise InsExc.InstanceException(f"request position id {p_id} is not appointed position")

    def init_part(self, ins: Instance, pst_id: int):
        flds_of_prt = ins.fields_of_part(pst_id)
        for f in flds_of_prt:
            ins.instances_fields.append(InstanceField(
                instance_id=ins.id,
                field_id=f.id,
                creator_id=self.cur_usr.id
            ))

    def delete_rsc_ins(self, rsc_ins):
        if rsc_ins.current_state != "initialized":
            raise ORMExc.IndelibleResourceInstance
        else:
            super().delete_rsc_ins(rsc_ins)


if __name__ == '__main__':
    from ORM.Model import User

    user1 = session.query(User).get(1)
    ins1 = session.query(Instance).get(1)
    ic1 = InstanceController(session, user1)
    ic1.patch_rsc_ins(rsc_ins=ins1, req_body={
        'instance_handle_request': {
            'handle': True,
            'handle_positions_id': [1, 2]
        }
    })
