from os import environ as env

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from python_outbox.sqlalchemy_outbox.sqlalchemy_storage_box import (
    SQLAlchemyStorageBoxMixin,
)

POSTGRES_HOST = env.get("POSTGRES_HOST", "localhost")
POSTGRES_PASSWORD = env.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_USER = env.get("POSTGRES_USER", "postgres")
POSTGRES_PORT = env.get("POSTGRES_PORT", "5432")
POSTGRES_DATABASE = env.get("POSTGRES_DATABASE", "user-service")

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, json_serializer=SQLAlchemyStorageBoxMixin.serializer
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
