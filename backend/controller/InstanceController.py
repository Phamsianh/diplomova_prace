from typing import List, Union, Optional

from ORM.Model import Form, InstanceField, Instance, Phase, Section, Receiver, Field, Director, User, UserPosition
from ORM.session import session
from controller.BaseController import BaseController
from exceptions import InstanceException as InsExc
from exceptions import ORMExceptions as ORMExc


class InstanceController(BaseController):
    related_resource = [
        "creator",
        "instances_fields",
        "directors",
        "receivers",
        "participants",
        "participated_users",
        "commits",
        "current_director",
        "current_receivers",
        "current_director_user",
        "current_receivers_users",
    ]

    def get_resource_collection(self, limit: Optional[int] = 50, offset: Optional[int] = 0, attribute: Optional[str] = None, value: Optional[str] = None, order: Optional[list] = None):
        """Get all instances in the system.

        Constraint:

        * Only admin can get all instance of the system.
        """
        if not self.current_user.is_admin:
            raise ORMExc.ORMException("require role admin for this endpoint")
        return super(InstanceController, self).get_resource_collection(limit, offset, attribute, value, order)

    def get_resource_instance(self, rsc_id: Union[str, int]):
        """Get the instance's information by id.

        Constraint:

        * Only participant of the instance can get the instance's information.
        """
        instance = super(InstanceController, self).get_resource_instance(rsc_id)
        if self.current_user not in instance.participants:
            raise ORMExc.ORMException("you are not a participant of this instance")
        return instance

    def post_resource_collection(self, req_body):
        """
To instantiate instance from a form and initialize the correspond administration process:

* The form must not be public or obsolete.
* Current authenticated user must have position designated for redirect the begin phase of the form.

Instance initialization includes:

* Set the ``current_phase_id`` of this instance to begin phase id.
* Create contents of begin fields, which are assigned for only authenticated user's position, with default value of an empty string. 
An empty string is necessary for hashing the corespond envelope.
* Set authenticated user to become the director of current phase.
* Set authenticated user to become the handler of only sections assigned for authenticated user's position.
"""
        val_body = self.get_val_dat(req_body, 'post')

        # check if form is public and obsolete
        form = self.session.query(Form).filter(Form.public == True, Form.id == val_body['form_id']).first()
        if not form:
            raise ORMExc.ResourceInstanceNotFound(Form, val_body['form_id'])
        if form.obsolete:
            raise InsExc.InstanceException("Form is obsolete")

        # check if user have assigned position for begin phase of the form and
        # set current phase of this instance to begin phase of the form
        begin_phase = form.begin_phase
        if begin_phase.position not in self.current_user.held_positions:
            raise InsExc.InstanceException("You can not init this form")
        new_ins = self.model(**val_body)
        new_ins.current_phase_id = begin_phase.id

        # create all contents of begin fields assigned for handler if any.
        begin_fields = self.session.query(Field).join(Field.section).\
            filter(
                Section.phase_id == begin_phase.id, 
                Section.position_id == begin_phase.position_id,
                ).all()
        for begin_field in begin_fields:
            new_ins.instances_fields.append(InstanceField(
                field_id=begin_field.id,
                creator_id=self.current_user.id
            ))
        new_ins.creator_id = self.current_user.id

        # set director of current phase to current authenticated user
        director = Director(instance=new_ins, phase=begin_phase, user=self.current_user)
        # set receiver of all sections assigned for authenticated user's position to current authenticated user.
        receivers = []
        begin_sections = self.session.query(Section).filter(
            Section.phase_id == begin_phase.id,
            Section.position_id == begin_phase.position_id
        ).all()
        for s in begin_sections:
            receivers.append(Receiver(instance=new_ins, section=s, user=self.current_user, received=True))

        try:
            self.session.add(new_ins)
            self.session.add(director)
            self.session.add_all(receivers)
            self.session.flush()
        except Exception as e:
            raise e
        else:
            self.session.commit()
            self.session.refresh(new_ins)
        return new_ins

    def patch_resource_instance(self, rsc_ins, req_body):
        """
Authenticated user, which is:

* Director of the current phase can transit instance to next phase.
* Receiver of the current phase can handle(receive) instance.
* Director of the end phase can mark the instance as 'done' to indicate the instance is completely handled.
---

# To transit instance:

## Constraints:

* User must be director of current phase.
* Requested next phase must be 1 of available next phases.
* Director must specify:

    * Who is director for next phase.
    * Director of next phase must be a potential director of next phase.

    * Who is receiver for each section of next phase.
    * Each user specified for each section must be potential handler of that section.
    * Then this section can only handled by specified user.
*Note: director and and receivers can be different*

## Transit instance include:

* Instance of current phase is committed.
* Change current phase of instance to requested next phase.
* Set user with ``id`` specified in ``director_id`` to be the director.
* Set users with ``id`` specified in ``receivers`` object to the receivers of sections of the next phase.

# To handle instance:

## Constraints:

* Only if user is receiver of instance at current phase.
Then all receiver's instance fields (contents) are auto created.

## Handle instance include:

* Auto created all receiver's instance fields (contents).
* Mark the ``received`` in receivers resource as ``true``.

*Note: The content cannot be manually created.*

# To mark the instance as done:

## Constraints:

* Only the director of the end phase can mark the instance as 'done'.
* The instance at state done cannot be modified.

---

"""
        val_body = self.get_val_dat(req_body, 'patch')
        
        if rsc_ins._current_state == "done":
            raise ORMExc.ORMException("the instance is completely handled.")
        if "done" in val_body and val_body["done"]:
            self.mark_instance_done(rsc_ins)
            self.session.commit()
            self.session.refresh(rsc_ins)
            return rsc_ins
        if "transit" in val_body:
            self.transit_instance(val_body["transit"], rsc_ins)
        if "handle" in val_body and val_body["handle"]:
            self.handle_instance(rsc_ins)
        self.session.commit()
        self.session.refresh(rsc_ins)
        return rsc_ins

    def mark_instance_done(self, ins: Instance):
        """To mark the instance as done:

        Constraints:

        * Only the director of the end phase can mark the instance as 'done'.
        * The instance at state done cannot be modified.
        """
        if ins.current_phase.phase_type != "end":
            raise ORMExc.ORMException("the current phase is not the end phase.")
        if self.current_user != ins.current_director_user:
            raise ORMExc.ORMException("you are not current director of this phase.")
        ins._current_state = "done"
        from ORM.Commiter import Committer
        committer = Committer(self.session, self.current_user, ins)
        committer.commit("Done.")

    def transit_instance(self, transit_data: dict, ins: Instance):
        """
        To transit instance:

        * User must be director of current phase.
        * Requested next phase must be 1 of available next phases.
        * Director must specify:

            * Who is director for next phase.
            * Director of next phase must be a potential director of next phase.
        
        * Director can specify:

            * Who is receivers for sections of next phase.
            * User specified for a section must be potential handler of that section.
            * Then this section can only handled by specified user.
        *Note: director and and receivers can be different*

        Transit instance include:

        * Instance of current phase is committed.
        * Change current phase of instance to requested next phase.
        * Set specified user with ``id`` = ``director_id`` to be the director
        * Set users with ``id`` specified in ``receivers`` object to the receivers of sections of the next phase.
        """

        # check if current user is director of current phase
        if ins.current_director_user != self.current_user:
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

            new_next_director_id = transit_data["director_id"]
            # check if next director is one of potential directors
            new_next_director_user = self.session.query(User).get(new_next_director_id)
            if new_next_director_user not in req_next_phase.potential_directors:
                raise ORMExc.ORMException(f"director {new_next_director_id} is not a potential directors")
            new_next_director = Director(instance_id=ins.id, phase_id=req_next_phase.id, user_id=new_next_director_id)

            # requested_receivers is a dictionary with key is section_id and with value is user_id
            # e.g. requested_receivers = { section_id: user_id }
            requested_receivers = transit_data["receivers"]
            avai_next_sections = req_next_phase.sections

            #  create Receiver instance for each section if specified any
            receivers = []
            for sct in avai_next_sections:
                # check if each section is specified in requested_receivers
                if sct.id not in requested_receivers:
                    continue
                # check if specified user is a potential handler for each section
                receiver_id = requested_receivers[sct.id]
                if receiver_id != 0:
                    receiver = self.session.query(User).get(receiver_id)
                    if receiver not in sct.potential_handlers:
                        raise ORMExc.ORMException(f"user {receiver_id} is not a potential handler of section {sct.id}")
                    receivers.append(Receiver(instance_id=ins.id, section_id=sct.id, user_id=receiver_id))

            self.session.add(new_next_director)
            self.session.add_all(receivers)
        else:
            receivers = []
            # if any receiver hasn't been specified yet and it is specified in requested_receiver, add new receiver
            for section_id, user_id in transit_data["receivers"].items():
                existed_receiver = self.session.query(Receiver).filter(
                    Receiver.instance_id == ins.id,
                    Receiver.section_id == section_id,
                ).first()
                if existed_receiver:
                    continue
                requested_section = self.session.query(Section).filter(
                    Section.id == section_id,
                    Section.phase_id == req_next_phase.id
                ).first()
                if not requested_section:
                    raise ORMExc.ORMException(f"section {section_id} does not belong to phase {req_next_phase.id}")
                potential_handler = self.session.query(User).join(User.users_positions).filter(
                    User.id == user_id,
                    UserPosition.position_id == requested_section.position_id
                ).first()
                if not potential_handler:
                    raise ORMExc.ORMException(f"user {user_id} is not a potential handler for section {section_id}")
                receivers.append(Receiver(instance_id=ins.id, section_id=section_id, user_id=user_id))

            self.session.add_all(receivers)

        from ORM.Commiter import Committer
        committer = Committer(self.session, self.current_user, ins)
        committer.commit(transit_data['message'])
        ins.current_phase_id = req_next_phase.id

    def handle_instance(self, ins: Instance):
        """
        Instance can be handled:

        * Only if user is receiver of instance at current phase.
        Then all receiver's sections are initialized.

        Handle instance include:

        * Initialize all receiver's fields.
        * Mark the ``received`` in receivers resource as ``true``.
        * Exchange key from instance's creator and handler. Thus handler can create envelopes to commit.
        """
        query = self.session.query(Field, Receiver).join(Field.section).join(Section.receivers).\
            filter(Receiver.instance_id == ins.id,
                   Section.phase_id == ins.current_phase_id,
                   Receiver.user_id == self.current_user.id,
                   Receiver.received == False).all()
        if not query:
            raise ORMExc.ORMException("you can not receive this instance")
        avai_fields, receiver = list(zip(*query))
        receivers = list(set(receiver))

        instances_fields = []
        for f in avai_fields:
            instances_fields.append(InstanceField(instance=ins, field=f, creator=self.current_user))
        for r in receivers:
            r.received = True
        self.session.add_all(instances_fields)

    def check_requested_positions(self, req_psts_id: List[int], ins: Instance):
        """
        User must holds all requested positions and all requested positions must be remaining positions.

        * ``req_psts_id``: positions, which user requests to handle specific parts of current phase.
        * ``ins``: instance, which is requested to be handle by user.
        """
        usr_psts_id = [pst.id for pst in self.current_user.held_positions]
        cur_rmn_psts_id = [pst.id for pst in ins.current_remaining_positions]
        for p_id in req_psts_id:
            if p_id not in usr_psts_id:
                raise ORMExc.ORMException(f"you're don't have position {p_id}")
            if p_id not in cur_rmn_psts_id:
                raise InsExc.InstanceException(f"request position id {p_id} is not appointed position")

    def init_sections(self, ins: Instance, sections_id: List[int]):
        init_field = self.session.query(Field).filter(Field.section_id.in_(sections_id)).all()
        for f in init_field:
            ins.instances_fields.append(InstanceField(
                instance_id=ins.id,
                field_id=f.id,
                creator_id=self.current_user.id
            ))

    def delete_resource_instance(self, rsc_ins):
        """Delete an instance.

        Constraint:

        * Authenticated user must be the owner of the form.
        * Instance can only be delete at begin phase without any commit."""

        # instance ownership of authenticated user is checked by method ``get_resource_instance``
        if rsc_ins.current_phase.phase_type != 'begin' or rsc_ins.commits:
            raise ORMExc.ORMException("instance can be deleted only at begin phase and without any commits.")
        return super(InstanceController, self).delete_resource_instance(rsc_ins)

    def get_instances_creator(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get creator of the instance.

        Constraint:

        * Only participants of the instance can retrieve its creator.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_instances_instances_fields(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all contents(s) of the instance.

        Constraint:

        * Only participants of the instance can retrieve its the contents.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_instances_directors(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all directors of the instance.

        Constraint:

        * Only participants of the instance can retrieve its directors.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_instances_receivers(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all receivers of the instance.

        Constraint:

        * Only participants of the instance can retrieve its receivers.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_instances_participants(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all current participants of the instance. 
        Participants include all directors and receivers of the instance.

        Constraint:

        * Only participants of the instance can retrieve its participants.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_instances_participated_users(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all participated users of the instance.
        Participated users include all users who've already became a creator of at least one of the envelope of the instance.
        That is, the user must be the last handler, who editted the content and the director must transit the instance to the next phase to create a commit.
        The system will create the envelope with the creator_id of the user, who is the last editor of the content.

        Constraint:

        * Only participants of the instance can retrieve its participants.
        """
        # Refer to the Commiter.create_envelope() method for more information.
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_instances_commits(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all commits of the instance.

        Constraint:

        * Only participants of the instance can retrieve its commits.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)
    
    def get_instances_current_director(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get current director of the instance.

        Constraint:

        * Only participants of the instance can retrieve its current director.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_instances_current_receivers(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all current receivers of the instance.

        Constraint:

        * Only participants of the instance can retrieve its current receivers.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)

    def get_instances_current_director_user(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get user, who is current director of the instance.

        Constraint:

        * Only participants of the instance can retrieve its user, who is the current director.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)
        
    def get_instances_current_receivers_users(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        """Get all users, who is current receivers of the instance.

        Constraint:

        * Only participants of the instance can retrieve its users, who is the current receivers.
        """
        return self.get_related_resource(rsc_id, rel_rsc, query)