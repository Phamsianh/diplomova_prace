import json
from typing import Optional, Union

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from ORM import Model
from ORM.session import Session
from exceptions import ORMExceptions as ORMExc
from pydantic_models import Schema
from utils.markdown_table_from_schema import create_markdown_table


class BaseController:
    """Class derived from this base class can declare following attributes:

    * ``controller_name`` is the base name for ``model``, ``post_schema``, ``patch_schema``, ``delete_schema``,
    ``response_schema``. Declare ``controller_name`` require to declare all attributes based on it.

    * ``model.__table__.name`` is the default name of resource. Declare resource name give it alias

    * ``related_resource`` is array of string, which contain all the keys of object's writable attributes of ``model``,
    excluding the attributes, whose keys begin with '_'. Declare this attribute to filter which related resource will
    be served as an endpoint.

    Class derived from this base class can overwrite methods:

    * ``get_resource_collection``
    * ``get_resource_instance``
    * ``get_related_resource``
    * ``post_resource_collection``
    * ``patch_resource_instance``
    * ``delete_resource_instance``
    to add more constraint and call to the correspond methods of the ``BaseController``. The docstring of overwritten
    methods is used as the description for the corresponding endpoint.

    Method ``get_related_resource`` can be overwritten for getting the related resource. The name of the method must
    follow the convention:
    get_{resource_name}_{related_resource}
    """

    def __init__(self, session: Session = None, current_user: Model.User = None):
        self.session = session
        self._current_user = current_user
        if not hasattr(self, "controller_name"):
            self.controller_name = self.__class__.__name__.removesuffix('Controller')
        if not hasattr(self, "model"):
            self.model = getattr(Model, self.controller_name)
        if not hasattr(self, "resource_name"):
            self.resource_name = self.model.__table__.name
        if not hasattr(self, "post_schema"):
            self.post_schema = getattr(Schema, self.controller_name + 'PostRequest')
        if not hasattr(self, "patch_schema"):
            self.patch_schema = getattr(Schema, self.controller_name + 'PatchRequest')
        if not hasattr(self, "delete_schema"):
            self.delete_schema = getattr(Schema, self.controller_name + 'DeleteRequest')
        if not hasattr(self, "response_schema"):
            self.response_schema = getattr(Schema, self.controller_name + 'Response')
        if not hasattr(self, "related_resource"):
            self.related_resource = [rr for rr in self.model.__dict__.keys() if rr[:1] != '_']
        if not hasattr(self, "post_schema_documentation"):
            self.post_schema_documentation = create_markdown_table(self.post_schema)
        if not hasattr(self, "patch_schema_documentation"):
            self.patch_schema_documentation = create_markdown_table(self.patch_schema)

    @property
    def current_user(self):
        return self._current_user

    @current_user.setter
    def current_user(self, current_user):
        self._current_user = current_user

    def get_resource_collection(self):
        rscs = self.session.query(self.model).limit(50).all()
        return rscs

    def get_resource_instance(self, rsc_id: Union[str, int]):
        if type(rsc_id) == str:
            if 'name' in self.model.__table__.controller_name.keys():
                # get resource instance by name
                rsc_ins = self.session.query(self.model).filter(self.model.name == rsc_id).first()
            else:
                raise ORMExc.ResourceCantSearchByName(self.resource_name)
        else:
            # get resource instance by id
            rsc_ins = self.session.query(self.model).get(rsc_id)
        if not rsc_ins:
            raise ORMExc.ResourceInstanceNotFound(self.model, rsc_id)
        else:
            return rsc_ins

    def get_related_resource(self, rsc_id: Union[str, int], rel_rsc, query: Optional[dict] = None):
        if rel_rsc not in self.related_resource:
            raise ORMExc.RelatedResourceNotFound(self.model, rel_rsc)
        rsc_ins = self.get_resource_instance(rsc_id)
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

    def post_resource_collection(self, req_body):
        val_body = self.get_val_dat(req_body, 'post')
        if hasattr(self.model, 'creator_id'):
            new_rsc_ins = self.model(**val_body, creator_id=self.current_user.id)
        else:
            new_rsc_ins = self.model(**val_body)
        self.session.add(new_rsc_ins)

        try:
            self.session.flush()
        except IntegrityError as e:
            if e.orig.pgcode == '23503':  # PostgreSQL Error Codes for FOREIGN KEY VIOLATION
                import re
                message_detail = e.orig.diag.message_detail
                _, rsc_ins_id = re.findall(r"\((.+?)\)", message_detail)
                rsc_name = e.orig.diag.table_name
                from ORM import Model_description
                r_m = Model_description.all_models[rsc_name]['model']
                raise ORMExc.ResourceInstanceNotFound(r_m, rsc_ins_id)
            elif e.orig.pgcode == '23505':  # PostgreSQL Error Codes for UNIQUE VIOLATION
                import re
                message_detail = e.orig.diag.message_detail
                att, val = re.findall(r"\((.+?)\)", message_detail)
                rsc_name = e.orig.diag.table_name
                raise ORMExc.ResourceInstanceExisted(rsc_name, att, val)
            else:
                raise
        else:
            self.session.commit()
            self.session.refresh(new_rsc_ins)
        return new_rsc_ins

    def patch_resource_instance(self, rsc_ins, req_body):
        val_body = self.get_val_dat(req_body, 'patch')
        for k, v in val_body.items():
            setattr(rsc_ins, k, v)
        try:
            self.session.flush()
        except IntegrityError:
            raise
        else:
            self.session.commit()
            self.session.refresh(rsc_ins)
        return rsc_ins

    def delete_resource_instance(self, rsc_ins):
        try:
            self.session.delete(rsc_ins)
            self.session.flush()
        except:
            raise
        else:
            self.session.commit()

    @staticmethod
    def prepare_response(rscs):
        """Get validated response from resource(s).\n
        If ``rscs`` is a collection of resource instances or a single resource instance,
        it'll be validated with pydantic model(schema).\n
        If ``rscs`` is an attribute of resource instance with built-in data type,
        return it directly.\n
        ``rscs``: Resource(s) can be: a collection of resource instances, a single resource instance or
        an attribute of resource instance. Resources must not be None.
        """
        from sqlalchemy.orm.collections import InstrumentedList
        from sqlalchemy.orm import DeclarativeMeta
        if isinstance(rscs, list) or isinstance(rscs, InstrumentedList):
            if rscs:
                if type(type(rscs[0])) == DeclarativeMeta:
                    # if resources is a collection of resource instances
                    res = []
                    response_schema = getattr(Schema, type(rscs[0]).__name__ + "Response")
                    for rsc in rscs:
                        try:
                            res.append(response_schema.from_orm(rsc))
                        except ValidationError as e:
                            raise ORMExc.ORMException(json.loads(e.json()))
                    return res
            else:
                # if resources is a collection of None
                return []
        elif type(type(rscs)) == DeclarativeMeta:
            # if resources is a single resource instance
            response_schema = getattr(Schema, type(rscs).__name__ + "Response")
            try:
                return response_schema.from_orm(rscs)
            except ValidationError as e:
                raise ORMExc.ORMException(json.loads(e.json()))
        elif type(type(rscs)) == type:
            # if resource(s) is an attribute of resource instance with built-in data type.
            return rscs
        else:
            raise TypeError(type(rscs))

    def get_val_dat(self, req_body: dict, req_mtd: str) -> dict:
        """
        Get validated data from request body data.\n
        ``req_body``: Request body data\n
        ``req_mtd``: Request method. Can be 'get', 'post', 'patch' or 'delete'
        """
        try:
            req_schema = getattr(self, f'{req_mtd}_schema')
            return req_schema(**req_body).dict(exclude_unset=True)
        except ValidationError as e:
            raise ORMExc.ORMException(json.loads(e.json()))
