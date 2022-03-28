from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from ORM.Model import User
from ORM.session import Session
from app_config import SECRET_KEY, ALGORITHM
from routes.dependencies.db import get_session
from routes.dependencies.oauth2_scheme import oauth2_scheme


class UserDependency:
    def __init__(self, token: Optional[str] = Depends(oauth2_scheme), session: Session = Depends(get_session)):
        self.token = token
        self.session = session
        # self.resource_instance_id = resource_instance_id

    def get_current_user(self) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = self.session.query(User).filter(User.user_name == username).first()
        if user is None:
            raise credentials_exception
        return user

        # user_name = decode_token(self.token)
        # user = self.session.query(User).filter(User.user_name == user_name).first()
        # if not user:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="username not found",
        #         headers={
        #             "www-authenticate": "bearer"
        #         }
        #     )
        # return user


# def decode_token(token: str):
#     return token
