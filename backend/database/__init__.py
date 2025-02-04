import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

engine = create_engine(
    f"postgresql+psycopg2://postgres:postgres@localhost:5432/investing",
    echo=True,
)

logger = logging.getLogger(__name__)

# Session constructor
Session = sessionmaker(autocommit=False, bind=engine)


def create_tables():
    """
    Create database tables from db models.
    """

    Base.metadata.create_all(engine)


def drop_tables():
    """
    Create database tables from db models.
    """

    Base.metadata.drop_all(engine)


def open_session():
    """
    Open and return a new db session
    """

    with Session() as session:
        yield session
