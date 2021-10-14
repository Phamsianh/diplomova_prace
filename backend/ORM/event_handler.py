from ORM import Model
from ORM.session import Session


def init_instance(ss: Session, obj):
    """
    When instance is initialized by user:
    ** current_phase_id must be id of begin phase
    ** all assigned sections and assigned fields for creator must be created automatically.
    **
    :param ss:
    :param obj:
    :return:
    """
    if type(obj) == Model.Instance:
        form = ss.query(Model.Form).get(obj.form_id)
        begin_phase = form.begin_phase
        obj.current_phase_id = begin_phase.id
        begin_fields = form.begin_fields
        for begin_field in begin_fields:
            obj.instances_fields.append(Model.InstanceField(
                field_id=begin_field.id,
                creator_id=obj.creator_id
            ))
