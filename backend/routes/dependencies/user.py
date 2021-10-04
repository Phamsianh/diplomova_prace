from fastapi import Depends, HTTPException, status, Path
from typing import Optional
from routes.dependencies.oauth2_scheme import oauth2_scheme
from routes.dependencies.db import get_session
from ORM.Model import User
from ORM.session import Session
from pydantic_models import Schema


class UserDependency:
    def __init__(self, token: Optional[str] = Depends(oauth2_scheme), session: Session = Depends(get_session)):
        self.token = token
        self.session = session
        # self.resource_instance_id = resource_instance_id

    def get_current_user(self) -> User:
        user_name = decode_token(self.token)
        user = self.session.query(User).filter(User.user_name == user_name).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="username not found",
                headers={
                    "www-authenticate": "bearer"
                }
            )
        return user

    # def get_user_by_username(self) -> Optional[User]:
    #     if not self.resource_instance_id:
    #         return None
    #     user = self.session.query(User).filter(User.user_name == self.resource_instance_id).first()
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="username not found"
    #         )
    #     return user


def get_current_user(
        token: Optional[str] = Depends(oauth2_scheme),
        session: Session = Depends(get_session)
) -> User:
    user_name = decode_token(token)
    user = session.query(User).filter(User.user_name == user_name).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="username not found",
            headers={
                "www-authenticate": "bearer"
            }
        )
    return user


def decode_token(token: str):
    return token


def validate_user_info(user_info: Schema.UserPostRequest):
    """not completely implement"""
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user info's not presented"
        )


def get_user_by_username(
        user_name: str = Path(...),
        session: Session = Depends(get_session)
) -> User:
    user = session.query(User).filter(User.user_name == user_name).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username not found"
        )
    return user


def require_admin_or_gr_admin_role(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin_or_gr_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This task require role admin or group admin. You don't have permission to do this task"
        )


def require_admin_role(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This task require role admin. You don't have permission to do this task"
        )


def require_gr_admin_role(
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_gr_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This task require role group admin. You don't have permission to do this task"
        )
