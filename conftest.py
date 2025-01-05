import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from core.main import app
from core.database import Base, SessionLocal
import settings


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        url=settings.DATABASE_URL,
        echo=True,
    )
    try:
        create_database(engine.url)
        Base.metadata.create_all(bind=engine)

        yield engine
        print("Database created!", engine)
        
    finally:
        engine.dispose()
        drop_database(engine.url)


@pytest.fixture(scope="function")
def db_session(db_engine):
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    )

    yield session

    session.rollback()
    session.close()
