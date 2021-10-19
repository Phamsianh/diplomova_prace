from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from ORM import Model_description
from ORM.session import Session
from exceptions import ORMExceptions as ORMExc
from pydantic_models import Schema
from routes.dependencies import oauth2_scheme as oa2s, db, user as u
from routes.helper import helper

router = APIRouter(
    tags=["all resources"],
    dependencies=[Depends(oa2s.oauth2_scheme)]
)


@router.delete("/{rsc}/{rsc_id}", status_code=status.HTTP_410_GONE)
def delete_rsc_instance(rsc: str, rsc_id: Union[int, str],
                        session: Session = Depends(db.get_session),
                        u_d: u.UserDependency = Depends()):
    try:
        helper.check_rsc_exist(rsc, Model_description.all_models.keys())
        rsc_model = Model_description.all_models[rsc]['model']
        req_schema = getattr(Schema, rsc_model.__name__ + "DeleteRequest")
        current_user = u_d.get_current_user()
        rsc_ins = helper.get_rsc_ins(rsc, rsc_id, session, u_d)
        helper.check_auth(req_schema, current_user, rsc_ins)
        helper.del_rsc_ins(rsc_ins)
    except ORMExc.IndelibleResourceInstance as e:
        raise HTTPException(405, e.message)
    except ORMExc.ORMException as e:
        raise HTTPException(400, e.message)
