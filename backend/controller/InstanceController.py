from typing import Optional, List
from ORM.session import session
from controller.BaseController import BaseController
from ORM.Model import Form, InstanceField, Instance, Phase, Section, Receiver, Field, User
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

        if "transit" in val_body:
            self.transit_instance(val_body["transit"], rsc_ins)
        if "handle" in val_body:
            self.handle_instance(rsc_ins, val_body["handle"])
        self.session.commit()
        self.session.refresh(rsc_ins)
        return rsc_ins

    def transit_instance(self, transit_data: dict, ins: Instance):
        """
        To transit instance:

        * User must be director of current phase.
        * Instance must have state 'full resolved'
        * Requested next phase must be 1 of available next phases
        * Director can specify:

            * Who can be handler of each section of next phase.
            Each user assigned for each section must be potential handler of that section.
            Then this section can only handled by assigned user.

            * If section is not assigned for a particular user:
             All potential handlers can handle this section and hence can view this instance.
             **Director of current phase must especially consider of this action.**


        Transit instance include:

        * Instance of current phase is committed.
        * Change current phase of instance to requested next phase
        * Assigned receivers to each section.
        """
        if ins.current_designated_position not in self.cur_usr.held_positions:
            raise InsExc.InstanceException("you're not director of this phase")

        ins_cur_state = ins.current_state
        if ins_cur_state != "full resolved":
            raise InsExc.CurrentPhaseNotResolved(ins_cur_state)

        req_next_phase = self.session.query(Phase).get(transit_data["current_phase_id"])
        avai_next_phases = ins.current_phase.next_phases
        if req_next_phase not in avai_next_phases:
            raise InsExc.NotAvailableNextPhases(transit_data["current_phase_id"], ins.id, avai_next_phases)

        requested_receivers = transit_data["receivers"]
        avai_next_sections = req_next_phase.sections
        if len(requested_receivers) >= len(avai_next_sections) :
            raise ORMExc.ORMException("number of receivers must be less than or "
                                      "equal to number of next available sections")

        receivers = []
        for r in requested_receivers:
            section = self.session.query(Section).get(r["section_id"])
            user = self.session.query(User).get(r["receiver_id"])
            if section not in avai_next_sections:
                raise ORMExc.ORMException(f"section {r.section_id} doesn't belong to phase {req_next_phase.id}")
            if user not in section.potential_handlers:
                raise ORMExc.ORMException(f"user {r['receiver_id']} is not a potential handler "
                                          f"of section {r['section_id']}")
            receivers.append(Receiver(instance_id=ins.id, section_id=r["section_id"], receiver_id=r["receiver_id"]))

        from ORM.Commiter import Committer
        committer = Committer(self.session, self.cur_usr, ins)
        committer.commit()
        ins.current_phase_id = req_next_phase.id
        self.session.add_all(receivers)

    def handle_instance(self, ins: Instance, sections_id: List[int]):
        """
        Instance can be handled:

        * If instance has current state: "pending" or "partial received" or "partial received & partial resolved"
        * If user is receiver of instance at current phase, initialize receiver's section.
        * If user is not a receiver but a potential handler, init potential handler's section

        Handle instance include:

        *  Initialize receiver's or potential handler's sections.
        *  Exchange key from instance's creator and handler. Thus handler can create envelopes to commit.
        """

        # if user is a receiver, requested sections must be 1 of remaining section specified for this user
        # if user is a potential handler, requested sections must be remaining sections and
        # user must hold position assigned for this section.
        if ins.current_state not in ["pending", "partial received", "partial received & partial resolved"]:
            raise InsExc.CurrentlyNotRequireHandle

        # for current user:
        held_positions = self.cur_usr.held_positions
        # current remaining specified sections id
        crt_rmn_scf_sct_id = [crr.section_id for crr in ins.current_remaining_receivers if crr.receiver_id == self.cur_usr.id]
        # current remaining sections id
        crt_rmn_sct_id = [crs.id for crs in ins.current_remaining_sections if crs.position in held_positions]
        if sections_id:
            for rsid in sections_id:
                if rsid not in crt_rmn_scf_sct_id and rsid not in crt_rmn_sct_id:
                    raise ORMExc.ORMException(f"section {rsid} is not specified or appointed for you")
            self.init_sections(ins, sections_id)
        else:
            if self.cur_usr in ins.current_remaining_receivers_users:
                self.init_sections(ins, crt_rmn_scf_sct_id)
            elif self.cur_usr in ins.current_potential_handlers:
                self.init_sections(ins, crt_rmn_sct_id)
            else:
                raise ORMExc.ORMException("you're not a potential handler or receiver of this instance")

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

    def init_sections(self, ins: Instance, sections_id: List[int]):
        init_field = self.session.query(Field).filter(Field.section_id.in_(sections_id)).all()
        for f in init_field:
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
