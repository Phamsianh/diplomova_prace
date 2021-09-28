import json
from typing import Any, Union, Optional
from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from ORM import Model_description
from ORM.Model import User
from ORM.session import Session
from pydantic_models import Schema
from routes.dependencies import user as u


def check_rsc_exist(rsc: str, all_rscs: list):
    if rsc not in all_rscs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"resource {rsc} doesn't exist. "
                                   f"available resources are {', '.join(all_rscs)}")


def check_auth(schema, current_user: User, rsc_ins: Optional[Any] = None):
    if hasattr(schema.Config, 'require_admin') and schema.Config.require_admin:
        if not current_user.is_admin:
            raise HTTPException(status_code=400, detail="require role admin")
    if hasattr(schema.Config, 'require_ownership') and schema.Config.require_ownership:
        check_ownership(rsc_ins, current_user)
    if hasattr(schema.Config, 'require_group_role') and schema.Config.require_group_role:
        check_group_role(rsc_ins, current_user)


def check_req_body(rsc: str, req_body: dict, req_schema):
    """
    check if the keys in request body exists in resource attributes
    :param rsc: resource name
    :param req_body: the request body
    :param req_schema: the schema of request resource
    :return: None
    """
    for r_b_k in req_body.keys():
        if r_b_k not in req_schema.__fields__.keys():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"resource {rsc} doesn't have attribute {r_b_k}. all attributes of {rsc} are "
                       f"{', '.join(req_schema.__fields__.keys())}"
                # TODO: which fields is required
            )


def get_val_dat(req_body: dict, req_schema, current_user: User) -> dict:
    try:
        if 'creator_id' in req_schema.__fields__.keys():
            req_body["creator_id"] = current_user.id
        return req_schema(**req_body).dict(exclude_unset=True)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=json.loads(e.json())
            # which fields is required
        )


def create_new_rsc_ins(val_data: dict, rsc_model, session: Session) -> Any:
    new_rsc_instance = rsc_model(**val_data)
    session.add(new_rsc_instance)
    try:
        session.flush()
    except IntegrityError as e:
        # TODO: For later consideration: refine the exception with which resource, which attributes cause the exception.
        #   research Exception from psycopg2, sqlalchemy,...
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="resource instance already exist")
    else:
        session.commit()
        session.refresh(new_rsc_instance)
    return new_rsc_instance


def get_res(rscs: Any) -> Any:
    """
    Get validated response from resource(s).
    If resource(s) is a collection of resource instances or a single resource instance,
    it'll be validated with pydantic model(schema). If it
    :param rscs: Resource(s) can be: a collection of resource instances, a single resource instance or
    an attribute of resource instance. Resources must not be None.
    :return: Validated response from resources
    """
    from sqlalchemy.orm.collections import InstrumentedList
    from sqlalchemy.orm import DeclarativeMeta
    if (type(rscs) == list or type(rscs) == InstrumentedList) and type(type(rscs[0])) == DeclarativeMeta:
        # if resources is a collection of resource instances
        rsc_schema = getattr(Schema, type(rscs[0]).__name__ + "Response")
        res = []
        for rsc in rscs:
            try:
                res.append(rsc_schema.from_orm(rsc))
            except ValidationError as e:
                raise HTTPException(status_code=400, detail=json.loads(e.json()))
        return res
    elif type(type(rscs)) == DeclarativeMeta:
        # if resources is a single resource instance
        rsc_schema = getattr(Schema, type(rscs).__name__ + "Response")
        try:
            return rsc_schema.from_orm(rscs)
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=json.loads(e.json()))
    elif type(type(rscs)) == type:
        # if resource(s) is an attribute of resource instance with built-in data type.
        return rscs
    else:
        raise TypeError(type(rscs))


def get_rsc_ins(rsc: str, rsc_id: Union[int, str], session: Session, usr_dep: u.UserDependency) -> Any:
    if type(rsc_id) == str:
        if rsc == 'users' and rsc_id == 'me':
            return usr_dep.get_current_user()

        rsc_model = Model_description.all_models[rsc]['model']
        if rsc == 'users':
            rsc_ins = session.query(rsc_model).filter(rsc_model.user_name == rsc_id).first()
        elif 'name' in rsc_model.__table__.c.keys():
            rsc_ins = session.query(rsc_model).filter(rsc_model.name == rsc_id).first()
        else:
            raise HTTPException(status_code=400,
                                detail=f"resource {rsc} can not be searched by name")

        if not rsc_ins:
            raise HTTPException(status_code=400,
                                detail=f"instance {rsc_id} of resource {rsc} doesn't exist")
        else:
            return rsc_ins
    elif type(rsc_id) == int:
        rsc_model = Model_description.all_models[rsc]['model']
        rsc_ins = session.query(rsc_model).get(rsc_id)
        if not rsc_ins:
            raise HTTPException(status_code=400,
                                detail=f"instance {rsc_id} of resource {rsc} doesn't exist")
        else:
            return rsc_ins


def get_rel_rsc(rsc_ins: Any, rel_rsc: str) -> Any:
    """
    Get related resource(s) of resource instance.
    :param rsc_ins: Resource instance
    :param rel_rsc: Related resource(s) can be a collection of resource instances, a single resource instance
    or an attribute of resource instance.
    :return: Related resource
    """
    # all available related resources of resource instance
    all_rel_rscs = [a for a in type(rsc_ins).__dict__.keys() if a[:1] != '_']
    if rel_rsc not in all_rel_rscs:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"resource {type(rsc_ins).__tablename__} doesn't have related resource {rel_rsc}. "
                                   f"related resource of {type(rsc_ins).__tablename__} are {', '.join(all_rel_rscs)}")
    return getattr(rsc_ins, rel_rsc)


def check_ownership(rsc_ins, current_user):
    all_rel_rscs = [a for a in type(rsc_ins).__dict__.keys() if a[:1] != '_']
    if 'creator' in all_rel_rscs:
        if rsc_ins.creator != current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail=f"you don't have ownership of this {rsc_ins.__tablename__} instance {rsc_ins.id}")
    elif type(rsc_ins) == type(current_user):
        if rsc_ins != current_user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                                detail=f"you don't own this account")
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{rsc_ins.__tablename__} doesn't have ownership")


def check_group_role(rsc_ins, current_user):
    all_rel_rscs = [a for a in type(rsc_ins).__dict__.keys() if a[:1] != '_']
    if 'group_role' in all_rel_rscs:
        if rsc_ins.group_role not in current_user.held_groups_roles:
            raise HTTPException(status_code=400,
                                detail=f"you must have group role {rsc_ins.group_role.name} to do this task")
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"resource {rsc_ins.__tablename__} doesn't have group role")


def upd_rsc_ins(val_dat: dict, rsc_ins: Any) -> Any:
    for k, v in val_dat.items():
        setattr(rsc_ins, k, v)
    session = inspect(rsc_ins).session
    try:
        session.flush()
    except IntegrityError:
        raise
    else:
        session.commit()
        session.refresh(rsc_ins)
    return rsc_ins


def del_rsc_ins(rsc_ins: Any):
    session = inspect(rsc_ins).session
    # TODO: delete user, form
    try:
        session.delete(rsc_ins)
        session.flush()
    except:
        raise
    else:
        session.commit()
