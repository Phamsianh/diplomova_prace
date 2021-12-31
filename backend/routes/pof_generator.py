from typing import Union
from fastapi import Depends, HTTPException, Request
from ORM.session import Session
from authentication.authorization.auth_checker import AuthorizationChecker
from exceptions import ORMExceptions as ORMExc, AuthCheckerException as ACExc
from routes.dependencies import db, user as u
import importlib


class POFGenerator:
    def __init__(self, ctl_name):
        self.rsc_ctlr_module = importlib.import_module(f'controller.{ctl_name}')
        self.rsc_ctlr_class = getattr(self.rsc_ctlr_module, ctl_name)
        self.rsc_ctlr = self.rsc_ctlr_class()
        self.response_schema = self.rsc_ctlr.response_schema

    #  Two request arrive at the same time try to concurrency modify session attribute of current rsc_ctlr,
    #  because FastAPI run path operation function in thread pool.
    #  So we must create new controller object for each path operation function to avoid concurrency

    def grc_generator(self):
        def get_resource_collection(session: Session = Depends(db.get_session)):
            try:
                # self.rsc_ctlr.session = session
                # rsc_col = self.rsc_ctlr.get_rsc_col()
                # return self.rsc_ctlr.get_res(rsc_col)
                rsc_ctlr = self.rsc_ctlr_class(session)
                rsc_col = rsc_ctlr.get_rsc_col()
                return rsc_ctlr.get_res(rsc_col)
            except ORMExc.ORMException as e:
                raise HTTPException(400, e.message)
        get_resource_collection.__name__ = f"get_{self.rsc_ctlr.rsc_name}_collection"
        get_resource_collection.__doc__ = self.rsc_ctlr.get_rsc_col.__doc__
        return get_resource_collection

    def gri_generator(self):
        def get_resource_instance(rsc_id: Union[int, str] = None,
                                  session: Session = Depends(db.get_session),
                                  u_d: u.UserDependency = Depends()):
            try:
                # self.rsc_ctlr.session = session
                # self.rsc_ctlr.cur_usr = u_d.get_current_user()
                # rsc_ins = self.rsc_ctlr.get_rsc_ins(rsc_id)
                # return self.rsc_ctlr.get_res(rsc_ins)
                rsc_ctlr = self.rsc_ctlr_class(session, u_d.get_current_user())
                rsc_ins = rsc_ctlr.get_rsc_ins(rsc_id)
                return rsc_ctlr.get_res(rsc_ins)
            except ORMExc.ORMException as e:
                raise HTTPException(400, e.message)
        get_resource_instance.__name__ = f"get_{self.rsc_ctlr.rsc_name}_instance"
        get_resource_instance.__doc__ = self.rsc_ctlr.get_rsc_ins.__doc__
        # self.response_schema = self.rsc_ctlr.response_schema
        return get_resource_instance

    def grr_generator(self, rel_r):
        def get_related_resource(*, rsc_id: Union[int, str] = None,
                                 req: Request,
                                 session: Session = Depends(db.get_session),
                                 u_d: u.UserDependency = Depends()):
            try:
                # self.rsc_ctlr.session = session
                # self.rsc_ctlr.cur_usr = u_d.get_current_user()
                # rel_rsc = self.rsc_ctlr.get_rel_rsc(rsc_id, rel_r, dict(req.query_params))
                # return self.rsc_ctlr.get_res(rel_rsc)
                rsc_ctlr = self.rsc_ctlr_class(session, u_d.get_current_user())
                rel_rsc = rsc_ctlr.get_rel_rsc(rsc_id, rel_r, dict(req.query_params))
                return self.rsc_ctlr.get_res(rel_rsc)
            except ORMExc.ORMException as e:
                raise HTTPException(400, e.message)
        get_related_resource.__name__ = f"get_{self.rsc_ctlr.rsc_name}_related_resource"
        get_related_resource.__doc__ = self.rsc_ctlr.get_rel_rsc.__doc__
        return get_related_resource

    def pr_generator(self):
        req_schema = self.rsc_ctlr.post_schema

        def post_resource(req_body: req_schema,
                          session: Session = Depends(db.get_session),
                          u_d: u.UserDependency = Depends()):
            try:
                # cur_usr = u_d.get_current_user()
                # self.rsc_ctlr.session = session
                # self.rsc_ctlr.cur_usr = u_d.get_current_user()
                # AuthorizationChecker(cur_usr, self.rsc_ctlr.post_schema).authorize()
                # new_rsc_ins = self.rsc_ctlr.post_rsc_ins(req_body.dict(exclude_unset=True))
                # return self.rsc_ctlr.get_res(new_rsc_ins)
                cur_usr = u_d.get_current_user()
                rsc_ctlr = self.rsc_ctlr_class(session, cur_usr)
                AuthorizationChecker(cur_usr, rsc_ctlr.post_schema).authorize()
                new_rsc_ins = rsc_ctlr.post_rsc_ins(req_body.dict(exclude_unset=True))
                return rsc_ctlr.get_res(new_rsc_ins)
            except (ORMExc.ORMException, ACExc.AuthCheckerException) as e:
                raise HTTPException(400, e.message)
        post_resource.__name__ = f"post_{self.rsc_ctlr.rsc_name}_resource"
        post_resource.__doc__ = self.rsc_ctlr.post_rsc_ins.__doc__
        return post_resource

    def pri_generator(self):
        req_schema = self.rsc_ctlr.patch_schema

        def patch_resource_instance(req_body: req_schema,
                                    rsc_id: Union[int, str] = None,
                                    session: Session = Depends(db.get_session),
                                    u_d: u.UserDependency = Depends()):
            try:
                # cur_usr = u_d.get_current_user()
                # self.rsc_ctlr.session = session
                # self.rsc_ctlr.cur_usr = u_d.get_current_user()
                # rsc_ins = self.rsc_ctlr.get_rsc_ins(rsc_id)
                # AuthorizationChecker(cur_usr, self.rsc_ctlr.patch_schema, rsc_ins).authorize()
                # upd_rsc_ins = self.rsc_ctlr.patch_rsc_ins(rsc_ins, req_body.dict(exclude_unset=True))
                # return self.rsc_ctlr.get_res(upd_rsc_ins)
                cur_usr = u_d.get_current_user()
                rsc_ctlr = self.rsc_ctlr_class(session, cur_usr)
                rsc_ins = rsc_ctlr.get_rsc_ins(rsc_id)
                AuthorizationChecker(cur_usr, rsc_ctlr.patch_schema, rsc_ins).authorize()
                upd_rsc_ins = rsc_ctlr.patch_rsc_ins(rsc_ins, req_body.dict(exclude_unset=True))
                return rsc_ctlr.get_res(upd_rsc_ins)
            except (ORMExc.ORMException, ACExc.AuthCheckerException) as e:
                raise HTTPException(400, e.message)
        patch_resource_instance.__name__ = f"patch_{self.rsc_ctlr.rsc_name}_resource_instance"
        patch_resource_instance.__doc__ = self.rsc_ctlr.patch_rsc_ins.__doc__
        return patch_resource_instance

    def dri_generator(self):

        def delete_resource_instance(rsc_id: Union[int, str],
                                     session: Session = Depends(db.get_session),
                                     u_d: u.UserDependency = Depends()):
            try:
                # cur_usr = u_d.get_current_user()
                # self.rsc_ctlr.session = session
                # self.rsc_ctlr.cur_usr = u_d.get_current_user()
                # rsc_ins = self.rsc_ctlr.get_rsc_ins(rsc_id)
                # AuthorizationChecker(cur_usr, self.rsc_ctlr.delete_schema, rsc_ins).authorize()
                # return self.rsc_ctlr.delete_rsc_ins(rsc_ins)
                cur_usr = u_d.get_current_user()
                rsc_ctlr = self.rsc_ctlr_class(session, cur_usr)
                rsc_ins = rsc_ctlr.get_rsc_ins(rsc_id)
                AuthorizationChecker(cur_usr, rsc_ctlr.delete_schema, rsc_ins).authorize()
                return rsc_ctlr.delete_rsc_ins(rsc_ins)
            except (ORMExc.ORMException, ACExc.AuthCheckerException) as e:
                raise HTTPException(400, e.message)

        delete_resource_instance.__name__ = f"delete_{self.rsc_ctlr.rsc_name}_resource_instance"
        delete_resource_instance.__doc__ = self.rsc_ctlr.delete_rsc_ins.__doc__

        return delete_resource_instance
