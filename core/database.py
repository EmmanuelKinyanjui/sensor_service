import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import settings


DATABASE_URL = settings.DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
