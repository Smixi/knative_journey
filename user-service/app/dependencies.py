from sqlalchemy.orm import Session

from .database import SessionLocal, engine


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
