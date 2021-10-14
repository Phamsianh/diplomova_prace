from fastapi import APIRouter, Depends, Body, HTTPException
from ORM.session import Session
from exceptions.ORMExceptions import ORMException
from routes.dependencies import oauth2_scheme as oa2s, db, user as u
from ORM import Model_description
from pydantic_models import Schema
from routes.helper import helper

router = APIRouter(
    dependencies=[Depends(oa2s.oauth2_scheme)],
    tags=["all resources"]
)


@router.post("/{rsc}")
def create_resource_instance(rsc: str, req_body: dict = Body(...), session: Session = Depends(db.get_session),
                             u_d: u.UserDependency = Depends()):
    try:
        helper.check_rsc_exist(rsc, Model_description.all_models.keys())
        rsc_model = Model_description.all_models[rsc]['model']
        req_schema = getattr(Schema, rsc_model.__name__ + "PostRequest")
        current_user = u_d.get_current_user()
        helper.check_auth(req_schema, current_user)
        helper.check_req_body(rsc, req_body, req_schema)

        val_data = helper.get_val_dat(req_body, req_schema, current_user)
        new_rsc_ins = helper.create_new_rsc_ins(val_data, rsc_model, session)
        return helper.get_res(new_rsc_ins)
    except ORMException as e:
        raise HTTPException(400, e.message)

# @router.post("/{resource}/{resource_instance_id}/{sub_resource}")
# def post_subordinate_resource(resource: str, resource_instance_id: Union[int, str], sub_resource: str,
#                               request_body: dict = Body(...), session: Session = Depends(db.get_session),
#                               u_d: u.UserDependency = Depends()):
#     # check if sup resource exists
#     sup_rsc = resource.lower()
#     check_sup_rsc_exist(sup_rsc, Model_description.sup_resource)
#     sup_rsc_mod = Model_description.all_models[sup_rsc]["model"]
#     current_user = u_d.get_current_user()
#     # check if sup resource instance exist
#     if sup_rsc == 'users' and resource_instance_id == "me":
#         sup_rsc_ins = current_user
#     else:
#         sup_rsc_ins = get_sup_rsc_ins(sup_rsc_mod, resource_instance_id, session)
#
#     # check if request sub resource is one of the sub resources of sup resource
#     sub_rsc = sub_resource.lower()
#     # sub_rsc_collection = Model_description.all_models[sup_rsc]["relationships"]["ONETOMANY"].keys()
#     # if sub_rsc not in sub_rsc_collection:
#     #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#     #                         detail=f"resource {sup_rsc} doesn't have subordinate resource {sub_rsc}. "
#     #                                f"subordinate resource of {sup_rsc} are {', '.join(sub_rsc_collection)}")
#     check_sub_rsc_exist(sup_rsc, sub_rsc)
#
#     # check if current user has authorization to create  sub resource
#     sub_rsc_mod = Model_description.all_models[sub_rsc]["model"]
#     req_schema = getattr(Schema,  sub_rsc_mod.__name__ + "Request")
#     # if hasattr(req_schema.Config, 'require_admin') and req_schema.Config.require_admin:
#     #     if not u_d.get_current_user().is_admin:
#     #         raise HTTPException(status_code=400, detail="require role admin")
#     check_auth(req_schema, current_user)
#
#     # check if request body follows request schema
#     # req_schema_fields = req_schema.__fields__.keys()
#     # for r_b_k in request_body.keys():
#     #     if r_b_k not in req_schema_fields:
#     #         raise HTTPException(status_code=400, detail=f"sub resource {sub_rsc} doesn't have attribute {r_b_k}. "
#     #                                                     f"Available attributes are {', '.join(req_schema_fields)}")
#     # try:
#     #     if 'creator_id' in req_schema.__fields__.keys():
#     #         request_body['creator_id'] = u_d.get_current_user().id
#     #     val_data = req_schema(**request_body).dict(exclude_unset=True)
#     # except ValidationError as e:
#     #     raise HTTPException(status_code=400, detail=json.loads(e.json()))
#     check_req_body(sub_rsc, request_body, req_schema)
#     request_body[f'{sup_rsc}_id'] = sup_rsc_ins.id
#     val_data = get_val_dat(request_body, req_schema, current_user)
#
#     # create new sub resource instance
#     # new_instance = sub_rsc_mod(**val_data)
#     # if "creator_id" in sub_rsc_mod.__table__.c.keys():
#     #     new_instance.creator_id = u_d.get_current_user().id
#     # session.add(new_instance)
#     # try:
#     #     session.commit()
#     # except IntegrityError:
#     #     raise HTTPException(status_code=400, detail="instance already exists")
#     # else:
#     #     session.refresh(new_instance)
#     new_sub_rsc_ins = create_new_rsc_ins(val_data, sub_rsc_mod, session)
#     res_schema = getattr(Schema, sub_rsc_mod.__name__ + "Response")
#     return get_res(res_schema, new_sub_rsc_ins)
#
#
# def check_sup_rsc_exist(sup_rsc: str, sup_rscs: list):
#     if sup_rsc not in sup_rscs:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail=f"resource {sup_rsc} doesn't exist or isn't a superior resource. "
#                                    f"all superior resources are {', '.join(sup_rscs)}")
#
#
# def get_sup_rsc_ins(sup_rsc_mod, sup_rsc_id: Union[str, int], session: Session) -> Any:
#     sup_rsc_ins = session.query(sup_rsc_mod).get(sup_rsc_id)
#     if not sup_rsc_ins:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail=f"{sup_rsc_mod.__tablename__} instance {sup_rsc_id} doesn't exist.")
#     return sup_rsc_ins
#
#
# def check_sub_rsc_exist(sup_rsc: str, sub_rsc: str):
#     sub_rscs = Model_description.all_models[sup_rsc]["relationships"]["ONETOMANY"].keys()
#     if sub_rsc not in sub_rscs:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail=f"resource {sup_rsc} doesn't have subordinate resource {sub_rsc}. "
#                                    f"subordinate resource of {sup_rsc} are {', '.join(sub_rscs)}")
#
#
# association_resources = {
#     "users_groups_roles": Model.UserGroupRole,
# }
#
#
# @router.post("/{resource}/{resource_instance_id}/{related_resource}/{related_resource_id}")
# def post_association_resource():
#     pass
