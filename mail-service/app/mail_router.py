from datetime import datetime
from http import HTTPStatus
from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.utils import EmailClient

from .dependencies import get_db, get_email_client
from .events import UserCreated, UserVerified
from .models import Events
from fastapi_cloudevents import CloudEvent
from fastapi_cloudevents.cloudevent_route import CloudEventRoute

logger = getLogger(__name__)

router = APIRouter(prefix="/mail", tags=["Mail"], route_class=CloudEventRoute)


@router.post("/welcome-user")
def send_mail_welcome_user(
    event: CloudEvent,
    db: Session = Depends(get_db),
    email_client: EmailClient = Depends(get_email_client),
):
    # Check we have the correct event type:
    if event.type != "UserCreated":
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, detail="The type of the event must be UserCreated"
        )

    # Check we can deserialize the internal event, if we can't we will never able to do action, so leave it.
    user_created_event = UserCreated(**event.data)
    # If it exist, it should be considered as acknowledged
    exists = db.query(Events).get(event.id)
    if exists is not None:
        return Response(status_code=HTTPStatus.OK)
    # Try to save the event
    db_event = Events(id=event.id, value=event)
    db.add(db_event)
    db.commit()
    try:
        email_client.send_mail(
            email=user_created_event.email,
            subject="Welcome !",
            body=f"Welcome {user_created_event.email}, You can activate your account using the token : {user_created_event.validation_token}",
        )
        db_event.treated = True
        db_event.treated_at = datetime.utcnow()
        db.add(db_event)
        db.commit()
    except Exception as exc:
        logger.exception("Cannot send mail", exc_info=exc)
    return Response(status_code=HTTPStatus.OK)


@router.post("/user-verified")
def send_mail_user_successfully_verified(
    event: CloudEvent,
    db: Session = Depends(get_db),
    email_client: EmailClient = Depends(get_email_client),
):
    # Check we have the correct event type:
    if event.type != "UserVerified":
        raise HTTPException(
            HTTPStatus.BAD_REQUEST, detail="The type of the event must be UserVerified"
        )

    # Check we can deserialize the internal event, if we can't we will never able to do action, so leave it.
    user_verified_event = UserVerified(**event.data)
    exists = db.query(Events).get(event.id)
    if exists is not None:
        return Response(status_code=HTTPStatus.OK)
    # Try to save the event
    db_event = Events(id=event.id, value=event)
    db.add(db_event)
    db.commit()
    try:
        email_client.send_mail(
            email=user_verified_event.email,
            subject="Welcome !",
            body=f"Welcome {user_verified_event.email}, Your account have been successfully verified",
        )
        db_event.treated = True
        db_event.treated_at = datetime.utcnow()
        db.add(db_event)
        db.commit()
    except Exception as exc:
        logger.exception("Cannot send mail", exc_info=exc)
    return Response(status_code=HTTPStatus.OK)
