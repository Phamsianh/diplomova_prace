from fastapi import APIRouter, Depends, Request, HTTPException

from exceptions.ORMExceptions import ORMException
from routes.dependencies import oauth2_scheme as oa2s, db, user as u
from ORM.session import Session
from ORM import Model_description
from typing import Union

from routes.helper import helper

router = APIRouter(
    dependencies=[Depends(oa2s.oauth2_scheme)],
    tags=["all resources"]
)


@router.get("/{rsc}")
def get_resource_collection(rsc: str, session: Session = Depends(db.get_session)):
    try:
        helper.check_rsc_exist(rsc, Model_description.all_models.keys())
        rsc_mod = Model_description.all_models[rsc]["model"]
        rsc_collection = session.query(rsc_mod).limit(50).all()
        return helper.get_res(rsc_collection)
    except ORMException as e:
        raise HTTPException(400, e.message)


@router.get("/{rsc}/{rsc_id}")
def get_resource_instance(rsc: str, rsc_id: Union[int, str], session: Session = Depends(db.get_session),
                          u_d: u.UserDependency = Depends()):
    try:
        helper.check_rsc_exist(rsc, Model_description.all_models.keys())
        rsc_ins = helper.get_rsc_ins(rsc, rsc_id, session, u_d)
        return helper.get_res(rsc_ins)
    except ORMException as e:
        raise HTTPException(400, e.message)


@router.get("/{rsc}/{rsc_id}/{rel_rsc}")
def get_related_resource_collection(rsc: str, rsc_id: Union[int, str], rel_rsc: str, req: Request,
                                    session: Session = Depends(db.get_session), u_d: u.UserDependency = Depends()):
    try:
        helper.check_rsc_exist(rsc, Model_description.all_models.keys())
        rsc_ins = helper.get_rsc_ins(rsc, rsc_id, session, u_d)
        rel_rscs = helper.get_rel_rsc(rsc_ins, rel_rsc, dict(req.query_params))
        # if not rel_rscs:
        #     return None
        # else:
        return helper.get_res(rel_rscs)
    except ORMException as e:
        raise HTTPException(400, e.message)
