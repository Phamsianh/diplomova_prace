from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Body
from ORM import Model_description
from ORM.session import Session
from pydantic_models import Schema
from routes.dependencies import oauth2_scheme as oa2s, db, user as u
from routes.helper import helper

router = APIRouter(
    tags=["all resources"],
    dependencies=[Depends(oa2s.oauth2_scheme)]
)


@router.patch("/{rsc}/{rsc_id}")
def update_rsc_instance(rsc: str, rsc_id: Union[int, str], req_body: dict = Body(...),
                        session: Session = Depends(db.get_session),
                        u_d: u.UserDependency = Depends()):
    helper.check_rsc_exist(rsc, Model_description.all_models.keys())
    rsc_model = Model_description.all_models[rsc]['model']
    req_schema = getattr(Schema, rsc_model.__name__ + "PatchRequest")
    current_user = u_d.get_current_user()
    rsc_ins = helper.get_rsc_ins(rsc, rsc_id, session, u_d)
    helper.check_auth(req_schema, current_user, rsc_ins)
    helper.check_req_body(rsc, req_body, req_schema)
    val_dat = helper.get_val_dat(req_body, req_schema, current_user)
    updated_rsc_ins = helper.upd_rsc_ins(val_dat, rsc_ins)
    return helper.get_res(updated_rsc_ins)
