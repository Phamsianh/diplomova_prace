from fastapi import APIRouter, Depends, Body, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from ORM.Model import User
from ORM.session import Session
from pydantic_models.Schema import UserResponse, UserRegistration
from routes.dependencies.db import get_session

registration_router = APIRouter()


@registration_router.post(
    "/registration",
    # response_model=UserResponse
)
def registration(
        session: Session = Depends(get_session),
        request_body: UserRegistration = Body(...,)
):
    """Registration

    * `first_name` is required. Must contain only letter and space

    * `last_name` is required. Must contain only letter and space

    * `user_name` is required. Must contain only uppercase or lowercase letter, space, number and special character -_!@#$%^&*()?{}

    * `password` is required. Must contain at least 8 characters, at least 1 uppercase letter, 1 lower letter, 1 number and can contain special character

    * `email` is required. Must follow email naming schema

    * `phone` is optional. Must only contain number

    * `birthdate` is optional. Must only contain datetime in
    """
    try:
        validated_data = request_body.dict(exclude_unset=True)
        new_user = User(**validated_data)
        session.add(new_user)
        session.commit()
    except ValidationError as e:
        return e.json()
    except IntegrityError as e:
        if e.orig.pgcode == '23505':  # PostgreSQL Error Codes for UNIQUE VIOLATION
            import re
            message_detail = e.orig.diag.message_detail
            att, val = re.findall(r"\((.+?)\)", message_detail)
            raise HTTPException(
                status_code=400,
                detail=f"'{att}' '{val}' already existed"
            )
    except Exception as e:
        raise e
    else:
        session.refresh(new_user)
        response = UserResponse.from_orm(new_user)
        return response
