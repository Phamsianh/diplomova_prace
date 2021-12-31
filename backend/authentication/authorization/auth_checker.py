from ORM import Model
from ORM.session import Session
from exceptions import AuthCheckerException as ACExc


class AuthorizationChecker:
    def __init__(self, cur_usr: Model.User, schema, rsc_ins=None):
        self.cur_usr = cur_usr
        self.schema = schema
        self.rsc_ins = rsc_ins

    def authorize(self):
        if hasattr(self.schema.Config, 'require_admin') and self.schema.Config.require_admin:
            if not self.cur_usr.is_admin:
                raise ACExc.RequireAdmin('require role admin')
        if hasattr(self.schema.Config, 'require_ownership') and self.schema.Config.require_ownership:
            all_rel_rscs = [a for a in type(self.rsc_ins).__dict__.keys() if a[:1] != '_']
            if 'creator' in all_rel_rscs:
                if self.rsc_ins.creator != self.cur_usr:
                    raise ACExc.RequireOwnership('require ownership')
            elif type(self.rsc_ins) == type(self.cur_usr):
                if self.rsc_ins != self.cur_usr:
                    raise ACExc.RequireOwnership('require ownership')
            else:
                raise ACExc.AuthCheckerException("resource doesn't have creator attribute")


if __name__ == '__main__':
    from ORM.session import session
    usr1 = session.query(Model.User).get(6)
    from pydantic_models import Schema
    form1 = session.query(Model.Form).get(1)
    ac1 = AuthorizationChecker(cur_usr=usr1, rsc_ins=form1, schema=Schema.FormPostRequest)

    print(ac1.authorize())
