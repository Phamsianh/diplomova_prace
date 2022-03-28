import hashlib
from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from ORM.Model import User
from ORM.session import session
from app_config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

token_router = APIRouter(
    tags=["authentication"]
)


@token_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get the token for authentication by username and password. Token will expire in 30 day from the moment of receiving."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(username: str, password: str) -> Union[bool, User]:
    user = session.query(User).filter(User.user_name == username).first()
    if not user:
        return False
    password = hashlib.sha256(password.encode()).hexdigest()
    if not password == user.password:
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
