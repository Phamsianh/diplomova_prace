import importlib
from typing import Optional, Union

from fastapi import Depends, HTTPException, Query, Request

from ORM.session import Session
from authentication.authorization.auth_checker import AuthorizationChecker
from exceptions import ORMExceptions as ORMExc, AuthCheckerException as ACExc
from routes.dependencies.db import get_session
from routes.dependencies.user import UserDependency


class POFGenerator:
    """
    Path Operation Function (POF) Generator has 6 methods, which generate POF for FastAPI from 6 methods of each controller.
    Each method of generator is where the authorization checker and controller interact with each other and
    is where the custom exceptions are caught.
    """

    def __init__(self, controller_name):
        self.controller_module = importlib.import_module(f'controller.{controller_name}')
        self.controller_class = getattr(self.controller_module, controller_name)
        self.controller = self.controller_class()
        self.response_schema = self.controller.response_schema

    #  Two request arrive at the same time try to concurrency modify session attribute of current ``controller``,
    #  because FastAPI run path operation function in thread pool.
    #  So we must create new controller object for each path operation function to avoid concurrency.

    def grc_generator(self):
        """Get Resource Collection Generator generates a get resource collection POF."""

        def get_resource_collection(session: Session = Depends(get_session),
                                    user_dependency: UserDependency = Depends(),
                                    limit: Optional[int] = Query(50, description="Limit number of results"),
                                    offset: Optional[int] = Query(0, description="Offset from which the result is queried"),
                                    attribute: Optional[str] = Query(None, description="Attribute of the resource"),
                                    value: Optional[str] = Query(None, description="Value of the attribute"),
                                    order: Optional[list] = Query(None, description="Name of attribute to sort")):
            try:
                current_user = user_dependency.get_current_user()
                controller = self.controller_class(session, current_user)
                resource_collection = controller.get_resource_collection(limit, offset, attribute, value, order)
                return controller.prepare_response(resource_collection)
            except ORMExc.ORMException as e:
                raise HTTPException(400, e.message)

        get_resource_collection.__name__ = f"get_{self.controller.resource_name}_collection"
        get_resource_collection.__doc__ = self.controller.get_resource_collection.__doc__
        return get_resource_collection

    def grcl_generator(self):
        """Get Resource Collection Generator generates a get resource collection length POF."""

        def get_resource_collection_length(session: Session = Depends(get_session),
                                            user_dependency: UserDependency = Depends(),
                                            attribute: Optional[str] = Query(None, description="Attribute of the resource"),
                                            value:Optional[str] = Query(None, description="Value of the attribute")):
            try:
                current_user = user_dependency.get_current_user()
                controller = self.controller_class(session, current_user)
                resource_collection_length = controller.get_resource_collection_length(attribute, value)
                return resource_collection_length
            except ORMExc.ORMException as e:
                raise HTTPException(400, e.message)

        get_resource_collection_length.__name__ = f"get_{self.controller.resource_name}_collection_length"
        get_resource_collection_length.__doc__ = self.controller.get_resource_collection_length.__doc__
        return get_resource_collection_length

    def gri_generator(self):
        """Get Resource Instance Generator generates a get resource instance POF."""

        def get_resource_instance(rsc_id: Union[int, str] = None,
                                  session: Session = Depends(get_session),
                                  user_dependency: UserDependency = Depends()):
            try:
                current_user = user_dependency.get_current_user()
                controller = self.controller_class(session, current_user)
                resource_instance = controller.get_resource_instance(rsc_id)
                AuthorizationChecker(current_user, controller.response_schema, resource_instance).authorize()
                return controller.prepare_response(resource_instance)
            except ORMExc.ORMException as e:
                raise HTTPException(400, e.message)

        get_resource_instance.__name__ = f"get_{self.controller.resource_name}_instance"
        get_resource_instance.__doc__ = self.controller.get_resource_instance.__doc__
        return get_resource_instance

    def grr_generator(self, related_resource):
        """Get Related Resource Generator generates a get related resource POF."""

        def get_related_resource(*, rsc_id: Union[int, str] = None,
                                 req: Request,
                                 session: Session = Depends(get_session),
                                 user_dependency: UserDependency = Depends()):
            try:
                controller = self.controller_class(session, user_dependency.get_current_user())
                if hasattr(controller, f"get_{self.controller.resource_name}_{related_resource}"):
                    # the method is get_related_resource is overwritten by the convention
                    rel_rsc = getattr(
                        controller,
                        f"get_{self.controller.resource_name}_{related_resource}"
                    )(rsc_id, related_resource, dict(req.query_params))
                else:
                    rel_rsc = controller.get_related_resource(rsc_id, related_resource, dict(req.query_params))
                return self.controller.prepare_response(rel_rsc)
            except (ORMExc.ORMException, ACExc.AuthCheckerException) as e:
                raise HTTPException(400, e.message)

        get_related_resource.__name__ = f"get_{self.controller.resource_name}_{related_resource}"
        if hasattr(self.controller, f"get_{self.controller.resource_name}_{related_resource}"):
            get_related_resource.__doc__ = getattr(
                self.controller,
                f"get_{self.controller.resource_name}_{related_resource}").__doc__
        return get_related_resource

    def prc_generator(self):
        """Post Resource Collection Generator generates a post resource collection POF."""
        req_schema = self.controller.post_schema

        def post_resource_collection(req_body: req_schema,
                                     session: Session = Depends(get_session),
                                     user_dependency: UserDependency = Depends()):
            try:
                current_user = user_dependency.get_current_user()
                controller = self.controller_class(session, current_user)
                # post to append a resource instance to collection is only require checking the admin role.
                AuthorizationChecker(current_user, controller.post_schema).authorize()
                new_resource_instance = controller.post_resource_collection(req_body.dict(exclude_unset=True))
                return controller.prepare_response(new_resource_instance)
            except (ORMExc.ORMException, ACExc.AuthCheckerException) as e:
                raise HTTPException(400, e.message)

        post_resource_collection.__name__ = f"post_{self.controller.resource_name}_resource"
        post_resource_collection.__doc__ = self.controller.post_resource_collection.__doc__ or ''
        post_resource_collection.__doc__ += self.controller.post_schema_documentation
        return post_resource_collection

    def pri_generator(self):
        """Patch Resource Instance Generator generates a patch resource instance POF."""
        req_schema = self.controller.patch_schema

        def patch_resource_instance(req_body: req_schema,
                                    rsc_id: Union[int, str] = None,
                                    session: Session = Depends(get_session),
                                    user_dependency: UserDependency = Depends()):
            try:
                current_user = user_dependency.get_current_user()
                controller = self.controller_class(session, current_user)
                resource_instance = controller.get_resource_instance(rsc_id)
                AuthorizationChecker(current_user, controller.patch_schema, resource_instance).authorize()
                updated_resource_instance = controller.patch_resource_instance(
                    resource_instance,
                    req_body.dict(exclude_unset=True)
                )
                return controller.prepare_response(updated_resource_instance)
            except (ORMExc.ORMException, ACExc.AuthCheckerException) as e:
                raise HTTPException(400, e.message)

        patch_resource_instance.__name__ = f"patch_{self.controller.resource_name}_resource_instance"
        patch_resource_instance.__doc__ = self.controller.patch_resource_instance.__doc__ or ''
        patch_resource_instance.__doc__ += self.controller.patch_schema_documentation

        return patch_resource_instance

    def dri_generator(self):
        """Delete Resource Instance Generator generates a delete resource instance POF."""

        def delete_resource_instance(rsc_id: Union[int, str],
                                     session: Session = Depends(get_session),
                                     user_dependency: UserDependency = Depends()):
            try:
                current_user = user_dependency.get_current_user()
                controller = self.controller_class(session, current_user)
                resource_instance = controller.get_resource_instance(rsc_id)
                AuthorizationChecker(current_user, controller.delete_schema, resource_instance).authorize()
                return controller.delete_resource_instance(resource_instance)
            except (ORMExc.ORMException, ACExc.AuthCheckerException) as e:
                raise HTTPException(400, e.message)

        delete_resource_instance.__name__ = f"delete_{self.controller.resource_name}_resource_instance"
        delete_resource_instance.__doc__ = self.controller.delete_resource_instance.__doc__

        return delete_resource_instance
