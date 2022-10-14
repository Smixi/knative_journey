from sqlalchemy.orm import Session

from app.utils import DummyEmailClient, EmailClient, SMTPEmailClient, EmailClassEnum
from .config import EMAIL_CLIENT
from .database import SessionLocal, engine


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_email_client() -> EmailClient:
    return EmailClassEnum[EMAIL_CLIENT].value()
