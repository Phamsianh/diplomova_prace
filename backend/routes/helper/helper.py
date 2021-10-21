import json
from typing import Any, Union, Optional, List
from fastapi import HTTPException, status
from pydantic import ValidationError
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from ORM import Model_description
from ORM.Model import User, Instance, Phase, InstanceField, Form, Group, Role, Position, Transition, Section, Field
from ORM.session import Session
from exceptions import ORMExceptions as ORMExc, InstanceException as InsExc
from pydantic_models import Schema
from routes.dependencies import user as u


def check_rsc_exist(rsc: str, all_rscs: list):
    if rsc not in all_rscs:
        raise ORMExc.ResourceNotExists(rsc, all_rscs)


def check_auth(schema, current_user: User, rsc_ins: Optional[Any] = None, action: Optional[str] = None ):
    if hasattr(schema.Config, 'require_admin') and schema.Config.require_admin:
        if not current_user.is_admin:
            raise ORMExc.RequireAdmin
    if hasattr(schema.Config, 'require_ownership') and schema.Config.require_ownership:
        check_ownership(rsc_ins, current_user)
    if hasattr(schema.Config, 'require_position') and schema.Config.require_position:
        check_position(rsc_ins, current_user)


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
            raise ORMExc.ResourceAttributeNotExists(rsc, r_b_k, req_schema.__fields__.keys())


def get_val_dat(req_body: dict, req_schema, current_user: User) -> dict:
    try:
        if 'creator_id' in req_schema.__fields__.keys():
            req_body["creator_id"] = current_user.id
        return req_schema(**req_body).dict(exclude_unset=True)
    except ValidationError as e:
        raise ORMExc.ORMException(json.loads(e.json()))


def create_new_rsc_ins(val_data: dict, rsc_model, session: Session, cur_usr: User) -> Any:
    from sqlalchemy import event
    from ORM import event_handler
    new_rsc_instance = rsc_model(**val_data)
    event.listen(session, 'transient_to_pending', event_handler.create_rsc_ins(cur_usr))
    session.add(new_rsc_instance)
    try:
        session.flush()
    except IntegrityError as e:
        if e.orig.pgcode == '23503':  # PostgreSQL Error Codes for FOREIGN KEY VIOLATION
            import re
            message_detail = e.orig.diag.message_detail
            _, rsc_ins_id = re.findall(r"\((.+?)\)", message_detail)
            rsc_name = re.search(r'"(.+?)"', message_detail).group(1)
            r_m = Model_description.all_models[rsc_name]['model']
            raise ORMExc.ResourceInstanceNotFound(r_m, rsc_ins_id)
        else:
            raise

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
                raise ORMExc.ORMException(json.loads(e.json()))
        return res
    elif type(type(rscs)) == DeclarativeMeta:
        # if resources is a single resource instance
        rsc_schema = getattr(Schema, type(rscs).__name__ + "Response")
        try:
            return rsc_schema.from_orm(rscs)
        except ValidationError as e:
            raise ORMExc.ORMException(json.loads(e.json()))
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
            raise ORMExc.ResourceCantSearchByName(rsc)

        if not rsc_ins:
            raise ORMExc.ResourceInstanceNotFound(rsc_model, rsc_id)
        else:
            return rsc_ins
    elif type(rsc_id) == int:
        rsc_model = Model_description.all_models[rsc]['model']
        rsc_ins = session.query(rsc_model).get(rsc_id)
        if not rsc_ins:
            raise ORMExc.ResourceInstanceNotFound(rsc_model, rsc_id)
        else:
            return rsc_ins


def get_rel_rsc(rsc_ins: Any, rel_rsc: str, query: Optional[dict] = None) -> Any:
    """
    Get related resource(s) of resource instance.
    :param rsc_ins: Resource instance
    :param rel_rsc: Related resource(s) can be a collection of resource instances, a single resource instance
    or an attribute of resource instance.
    :param query: An optional dict of query parameters. If related resource have type method and requires arguments
    query must be presented.
    :return: Related resource
    """
    # all available related resources of resource instance
    all_rel_rscs = [a for a in type(rsc_ins).__dict__.keys() if a[:1] != '_']
    if rel_rsc not in all_rel_rscs:
        raise ORMExc.RelatedResourceNotFound(type(rsc_ins), rel_rsc)
    rr = getattr(rsc_ins, rel_rsc)
    if type(rr).__name__ == 'method':
        from inspect import getfullargspec
        method_args = getfullargspec(rr)[0][1:]
        if method_args and not query:
            raise HTTPException(status_code=400,
                                detail=f"This endpoint require query parameters {', '.join(method_args)}")
        try:
            from pydantic import validate_arguments
            rr = validate_arguments(rr)
            return rr(**query)
        except ValidationError as e:
            raise ORMExc.ORMException(json.loads(e.json()))
    else:
        return rr


def check_ownership(rsc_ins, current_user):
    all_rel_rscs = [a for a in type(rsc_ins).__dict__.keys() if a[:1] != '_']
    if 'creator' in all_rel_rscs:
        if rsc_ins.creator != current_user:
            raise ORMExc.RequireOwnership
    elif type(rsc_ins) == type(current_user):
        if rsc_ins != current_user:
            raise ORMExc.RequireOwnership
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{rsc_ins.__tablename__} doesn't have ownership")


def check_position(rsc_ins, current_user):
    all_rel_rscs = [a for a in type(rsc_ins).__dict__.keys() if a[:1] != '_']
    if 'position' in all_rel_rscs:
        if rsc_ins.position not in current_user.held_groups_roles:
            raise HTTPException(status_code=400,
                                detail=f"you must have group role {rsc_ins.position.name} to do this task")
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"resource {rsc_ins.__tablename__} doesn't have group role")


def upd_rsc_ins(val_dat: dict, rsc_ins: Any, session: Session, current_user: User) -> Any:
    # handlers update fields
    if type(rsc_ins) == Instance:
        update_instance(val_dat, rsc_ins, session, current_user)
    else:
        for k, v in val_dat.items():
            setattr(rsc_ins, k, v)
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
    # TODO: delete users_positions
    rsc_ins_type = type(rsc_ins)
    if rsc_ins_type == User \
            or (rsc_ins_type in [Form, Phase, Transition, Section, Field]) and rsc_ins.public \
            or (rsc_ins_type == Instance and rsc_ins.current_state != "initialized") \
            or (rsc_ins_type == Group and rsc_ins.joiners is not None) \
            or (rsc_ins_type == Role and rsc_ins.holders is not None) \
            or (rsc_ins_type == Position and rsc_ins.holders is not None):
        raise ORMExc.IndelibleResourceInstance

    try:
        session.delete(rsc_ins)
        session.flush()
    except:
        raise
    else:
        session.commit()


def update_instance(val_dat: dict, ins: Instance, ses: Session, cur_usr: User):
    if "current_phase_id" in val_dat:
        transit_instance(val_dat["current_phase_id"], ins, ses, cur_usr)
    if "instance_handle_request" in val_dat and val_dat["instance_handle_request"]["handle"]:
        handle_instance(
            ins,
            cur_usr,
            val_dat["instance_handle_request"]["handled_positions_id"]
            if "handled_positions_id" in val_dat["instance_handle_request"]
            else None)


def transit_instance(cur_phs_id: int, ins: Instance, ses: Session, cur_usr: User):
    if ins.current_designated_position not in cur_usr.held_positions:
        raise HTTPException(400, "you're not director of this phase")
    else:
        ins_cur_state = ins.current_state
        if ins_cur_state != "full resolved":
            raise InsExc.CurrentPhaseNotResolved(ins_cur_state)
        else:
            req_next_phase = ses.query(Phase).get(cur_phs_id)
            avai_next_phases = ins.current_phase.next_phases
            if req_next_phase not in avai_next_phases:
                raise InsExc.NotAvailableNextPhases(cur_phs_id, ins.id, avai_next_phases)
            else:
                ins.current_phase_id = req_next_phase.id


def handle_instance(ins: Instance, cur_usr: User, req_psts_id: Optional[List[int]]):
    check_ins_cur_state(ins)
    if req_psts_id:
        check_req_psts(req_psts_id, cur_usr, ins)
        val_req_psts_id = req_psts_id
    else:
        val_req_psts_id = [pst.id for pst in ins.current_remaining_positions if pst in cur_usr.held_positions]
    for p_id in val_req_psts_id:
        init_part(ins, cur_usr, p_id)


def check_ins_cur_state(ins: Instance):
    ins_cur_state = ins.current_state
    if ins_cur_state not in ["pending", "partial received", "partial received & partial resolved"]:
        raise InsExc.CurrentlyNotRequireHandle


def check_req_psts(req_psts_id: List[int], usr: User, ins: Instance):
    """
    User must own all request positions and all request positions must be remaining positions.
    :param req_psts_id: positions, which user request to handle specific parts of current phase.
    :param usr: user, who request to handle instance.
    :param ins: instance, which is requested to be handle by user.
    :return: None
    """
    usr_psts_id = [pst.id for pst in usr.held_positions]
    cur_rmn_psts_id = [pst.id for pst in ins.current_remaining_positions]
    for p_id in req_psts_id:
        if p_id not in usr_psts_id:
            raise ORMExc.RelatedResourceInstanceNotFound(usr, "held_positions", p_id)
        if p_id not in cur_rmn_psts_id:
            raise HTTPException(400, f"request position id {p_id} is not appointed position")


def init_part(ins: Instance, cur_usr: User, pst_id: int):
    flds_of_prt = ins.fields_of_part(pst_id)
    for f in flds_of_prt:
        ins.instances_fields.append(InstanceField(
            instance_id=ins.id,
            field_id=f.id,
            creator_id=cur_usr.id
        ))
