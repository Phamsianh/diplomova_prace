from typing import Type

from pydantic import BaseModel

from ORM.Base import Base
from ORM.Model import User
from exceptions import AuthCheckerException as ACExc


class AuthorizationChecker:
    """
    The AuthorizationChecker is used for:

    * Checking the role of the user in specific operation on a resource, for example: only admin can create an administration process and form.

    * Checking if the user has the ownership on a resource instance, for example: user can only change their own password.

    AuthorizationChecker use 4 schemas provided by BaseController, those are post_schema, patch_schema, delete_schema,
    response_schema, for its checking authorization.
    """

    def __init__(self, current_user: User, schema: Type[BaseModel], resource_instance: Type[Base] = None):
        """

        :param current_user: the current user
        :param schema: the schema used for checking authorization
        :param resource_instance: if ``schema.Config`` have attribute ``require_ownership``, this parameter must be provided
        """
        self.current_user = current_user
        self.schema = schema
        self.resource_instance = resource_instance

    def authorize(self):
        if hasattr(self.schema.Config, 'require_admin') and self.schema.Config.require_admin:
            if not self.current_user.is_admin:
                raise ACExc.RequireAdmin('require role admin')
        if hasattr(self.schema.Config, 'require_ownership') and self.schema.Config.require_ownership:
            all_rel_rscs = [a for a in type(self.resource_instance).__dict__.keys() if a[:1] != '_']
            if 'creator' in all_rel_rscs:
                if self.resource_instance.creator != self.current_user:
                    raise ACExc.RequireOwnership('require ownership')
            elif isinstance(self.resource_instance, User):
                if self.resource_instance != self.current_user:
                    raise ACExc.RequireOwnership('require ownership')
            else:
                raise ACExc.AuthCheckerException("resource doesn't have creator attribute")
