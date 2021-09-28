from sqlalchemy import event
from ORM import Model
from ORM.session import session
from fastapi import HTTPException


@event.listens_for(session, 'transient_to_pending')
def intercept_transient_to_pending(ss, obj):
    if type(obj) == Model.FormInstance:
        begin_phase = ss.query(Model.Phase).join(Model.Phase.form).filter(Model.Form.id == obj.form_id).\
            filter(Model.Phase.phase_type == 'begin').first()
        if not begin_phase:
            raise HTTPException(status_code=400, detail=f"Form instance {obj.form_id} doesn't exist")
        obj.current_phase_id = begin_phase.id
