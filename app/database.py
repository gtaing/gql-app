import os
import logging
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session, sessionmaker
from app.data import employers_data, jobs_data
from app.models import Employer, Job, Base

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:Georgio#2024@host.docker.internal:5432/jobboard",
)

engine = create_engine(DB_URL)


def clear_db_content() -> None:
    logging.info("Clearing database content.")
    with Session(engine) as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


def loading_employers() -> None:
    logging.info("Loading employers data.")
    with Session(engine) as session:
        for employer in employers_data:
            try:
                session.add(Employer(**employer))
            except:
                pass
        session.commit()


def loading_jobs() -> None:
    logging.info("Loading jobs data.")
    with Session(engine) as session:
        for job in jobs_data:
            try:
                session.add(Job(**job))
            except:
                pass
        session.commit()


def loading_data() -> None:
    Base.metadata.create_all(bind=engine)

    clear_db_content()

    loading_employers()
    loading_jobs()


def get_session():
    session = sessionmaker(bind=engine)
    db = session()

    db.commit()

    try:
        yield db
    finally:
        db.close()
