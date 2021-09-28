from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ORM.Model import User
from ORM.session import session
import hashlib

token_router = APIRouter(
    tags=["authentication"]
)


@token_router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    user = session.query(User).filter(User.user_name == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username or password")

    password = hashlib.sha256(form_data.password.encode()).hexdigest()
    if not password == user.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    return {"access_token": user.user_name, "token_type": "bearer"}
