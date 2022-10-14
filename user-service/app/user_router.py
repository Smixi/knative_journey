from enum import Enum
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from jwt import ExpiredSignatureError, InvalidTokenError
from python_outbox.sqlalchemy_outbox.sqlalchemy_storage_box import (
    SQLAlchemyPydanticStorageBox,
)
from sqlalchemy.orm import Session

from .dependencies import get_db
from .events import UserCreated, UserVerified
from .models import (
    AccountAlreadyVerified,
    NotValidToken,
    User,
    UserDoesNotExist,
    generate_token_for_user,
    verify_user_token,
)
from .schemas import UserIn, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.post("/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).count():
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail="User already exists")
    db_user = User(email=user.email, password=user.password)
    db.add(db_user)
    db.flush()
    db_user.validation_token = generate_token_for_user(db_user.id, db_user.email)
    db_user_created_event = SQLAlchemyPydanticStorageBox(
        UserCreated(
            id=db_user.id, email=user.email, validation_token=db_user.validation_token
        )
    )
    db.add_all([db_user_created_event, db_user])
    db.commit()
    return db_user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).get(user_id)
    if db_user is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="User does not exists")
    return db_user


@router.post("/verify", status_code=HTTPStatus.NO_CONTENT)
def verify_user(token: str, db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, detail="You must provide the token to be verified"
        )
    try:
        db_user = verify_user_token(token, db)
    except (NotValidToken, AccountAlreadyVerified, UserDoesNotExist) as exc:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=str(exc))
    db_user_verified_event = SQLAlchemyPydanticStorageBox(
        UserVerified(id=db_user.id, email=db_user.email)
    )
    db.add(db_user_verified_event)
    db.commit()
