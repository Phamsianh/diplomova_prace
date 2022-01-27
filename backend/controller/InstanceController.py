from typing import Optional, List
from ORM.session import session
from controller.BaseController import BaseController
from ORM.Model import Form, InstanceField, Instance, Phase, Section, Receiver, Field, User, Director
from exceptions import ORMExceptions as ORMExc
from exceptions import InstanceException as InsExc


class InstanceController(BaseController):
    def post_rsc_ins(self, req_body):
        """
        To create (initialize) instance from a form, the form must not be public or obsolete.
        Instance initialization includes:

        * Set the current phase of this instance to begin phase of the form if user have assigned position.
        * Create all begin fields with value is null.
        * Set director of current phase to current user
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

        # set director of current phase to current user
        director = Director(instance=new_ins, phase=begin_phase, user=self.cur_usr)

        try:
            self.session.add(new_ins)
            self.session.add(director)
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
        if "handle" in val_body and val_body["handle"]:
            self.handle_instance(rsc_ins)
        self.session.commit()
        self.session.refresh(rsc_ins)
        return rsc_ins

    def transit_instance(self, transit_data: dict, ins: Instance):
        """
        To transit instance:

        * User must be director of current phase.
        * Requested next phase must be 1 of available next phases
        * Director must specify:

            Who is director for next phase.
            Director of next phase must be one of receivers.
            Director of next phase must be a potential director of next phase.

            Who is receiver for each section of next phase.
            Each user assigned for each section must be potential handler of that section.
            Then this section can only handled by assigned user.

        Transit instance include:

        * Instance of current phase is committed.
        * Change current phase of instance to requested next phase
        * Assigned receivers to each section.
        """

        # check if current user is director of current phase
        if ins.current_director != self.cur_usr:
            raise InsExc.InstanceException("you're not director of this phase")

        # check if requested next phase is 1 of available phases
        req_next_phase = self.session.query(Phase).get(transit_data["current_phase_id"])
        avai_next_phases = ins.current_phase.next_phases
        if req_next_phase not in avai_next_phases:
            raise InsExc.NotAvailableNextPhases(transit_data["current_phase_id"], ins.id, avai_next_phases)

        # check if next phase has been already received
        next_director = session.query(Director).filter(Director.instance_id == ins.id,
                                                       Director.phase_id == req_next_phase.id).first()
        if not next_director:
            # director_id and receivers must be defined:
            if "director_id" not in transit_data or "receivers" not in transit_data:
                raise ORMExc.ORMException("next phase has not been received. "
                                          "director_id and receivers_id must be specified")
            # check if director is one of receivers
            new_next_director_id = transit_data["director_id"]
            # requested_receivers is a dictionary with key is section_id and with value is user_id
            # e.g. requested_receivers = { section_id: user_id }
            requested_receivers = transit_data["receivers"]
            if new_next_director_id not in requested_receivers.values():
                raise ORMExc.ORMException("director of next phase must be one of the receivers")

            # check if director is one of potential directors
            new_next_director_user = self.session.query(User).get(new_next_director_id)
            if new_next_director_user not in req_next_phase.potential_directors:
                raise ORMExc.ORMException(f"director {new_next_director_id} is not a potential directors")
            new_next_director = Director(instance_id=ins.id, phase_id=req_next_phase.id, user_id=new_next_director_id)

            # number of receivers must equal to number of sections in next phase
            avai_next_sections = req_next_phase.sections
            if len(requested_receivers) != len(avai_next_sections):
                raise ORMExc.ORMException("number of receivers must be equal to number of next available sections")

            #  create Receiver instance for each section
            receivers = []
            for sct in avai_next_sections:
                # check if each section is specified in requested_receivers
                if sct.id not in requested_receivers:
                    raise ORMExc.ORMException(f"section {sct.id} must be specified")
                # check if specified user is a potential handler for each section
                receiver_id = requested_receivers[sct.id]
                receiver = self.session.query(User).get(receiver_id)
                if receiver not in sct.potential_handlers:
                    raise ORMExc.ORMException(f"user {receiver_id} is not a potential handler of section {sct.id}")
                receivers.append(Receiver(instance_id=ins.id, section_id=sct.id, user_id=receiver_id))

            self.session.add(new_next_director)
            self.session.add_all(receivers)

        from ORM.Commiter import Committer
        committer = Committer(self.session, self.cur_usr, ins)
        committer.commit()
        ins.current_phase_id = req_next_phase.id

    def handle_instance(self, ins: Instance):
        """
        Instance can be handled:

        * Only if user is receiver of instance at current phase.
        Then all receiver's sections are initialized.

        Handle instance include:

        *  Initialize all receiver's fields.
        *  Exchange key from instance's creator and handler. Thus handler can create envelopes to commit.
        """
        query = self.session.query(Field, Receiver).join(Field.section).join(Section.receivers).\
            filter(Receiver.instance_id == ins.id,
                   Section.phase_id == ins.current_phase_id,
                   Receiver.user_id == self.cur_usr.id,
                   Receiver.received == False).all()
        if not query:
            raise ORMExc.ORMException("you can not receive this instance")
        avai_fields, receiver = list(zip(*query))
        receivers = list(set(receiver))

        instances_fields = []
        for f in avai_fields:
            instances_fields.append(InstanceField(instance=ins, field=f, creator=self.cur_usr))
        for r in receivers:
            r.received = True
        self.session.add_all(instances_fields)

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
