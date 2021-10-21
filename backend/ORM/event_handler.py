from ORM import Model
from ORM.session import Session
from exceptions.InstanceException import InstanceException
from exceptions import ORMExceptions as ORMExc


def create_rsc_ins(cur_usr: Model.User):
    def c_r_i(ses: Session, obj):
        """
        When instance is initialized by user:
        ** current_phase_id must be id of begin phase
        ** all assigned sections and assigned fields for creator must be created automatically.
        **
        :param ses:
        :param obj:
        :return:
        """
        type_rsc_ins = type(obj)
        # init instance
        if type_rsc_ins == Model.Instance:
            form = ses.query(Model.Form).filter(Model.Form.public == True, Model.Form.id == obj.form_id).first()
            if not form:
                raise ORMExc.ResourceInstanceNotFound(Model.Form, obj.form_id)
            if form.obsolete:
                raise InstanceException("Form is obsolete")
            begin_phase = form.begin_phase
            if begin_phase.position not in cur_usr.held_positions:
                raise InstanceException("You can not init this form")
            obj.current_phase_id = begin_phase.id
            begin_fields = form.begin_fields
            for begin_field in begin_fields:
                obj.instances_fields.append(Model.InstanceField(
                    field_id=begin_field.id,
                    creator_id=obj.creator_id
                ))

        # create users_positions
        if type_rsc_ins == Model.UserPosition:
            assigned_pst = ses.query(Model.Position).get(obj.position_id)
            if not assigned_pst:
                raise ORMExc.ResourceInstanceNotFound(Model.Position, obj.position_id)
            if assigned_pst.creator != cur_usr:
                raise ORMExc.RequireOwnership
            assigned_usr = ses.query(Model.User).get(obj.user_id)
            if not assigned_usr:
                raise ORMExc.ResourceInstanceNotFound(Model.User, obj.user_id)

        # create phase
        if type_rsc_ins == Model.Phase:
            form = ses.query(Model.Form).get(obj.form_id)
            if not form:
                raise ORMExc.ResourceInstanceNotFound(Model.Form, obj.form_id)
            if cur_usr != form.creator:
                raise ORMExc.RequireOwnership
            if form.public:
                raise ORMExc.ORMException("Form is public")

        # create transition
        if type_rsc_ins == Model.Transition:
            if obj.from_phase_id == obj.to_phase_id:
                raise ORMExc.ORMException("from phase and to phase must not be the same")

            from_phase = ses.query(Model.Phase).get(obj.from_phase_id)
            if not from_phase:
                raise ORMExc.ResourceInstanceNotFound(Model.Phase, obj.from_phase_id)
            if from_phase.creator != cur_usr:
                raise ORMExc.RequireOwnership

            to_phase = ses.query(Model.Phase).get(obj.to_phase_id)
            if not to_phase:
                raise ORMExc.ResourceInstanceNotFound(Model.Phase, obj.to_phase_id)
            if from_phase.creator != cur_usr:
                raise ORMExc.RequireOwnership

            if from_phase.form != to_phase.form:
                raise ORMExc.ORMException("from phase and to phase must belong to one form")
            if from_phase.form.public:
                raise ORMExc.ORMException("Form is public")

        # create section
        if type_rsc_ins == Model.Section:
            phase = ses.query(Model.Phase).get(obj.phase_id)
            if not phase:
                raise ORMExc.ResourceInstanceNotFound(Model.Phase, obj.phase_id)
            if cur_usr != phase.form.creator:
                raise ORMExc.RequireOwnership
            if phase.form.public:
                raise ORMExc.ORMException("Form is public")

        # create field
        if type_rsc_ins == Model.Field:
            section = ses.query(Model.Section).get(obj.section_id)
            if not section:
                raise ORMExc.ResourceInstanceNotFound(Model.Phase, obj.section_id)
            form = section.form
            if cur_usr != form.creator:
                raise ORMExc.RequireOwnership
            if form.public:
                raise ORMExc.ORMException("Form is public")

    return c_r_i
