import os
import logging
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from app.db.data import employers_data, jobs_data
from app.db.models import Employer, Job, Base

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:Georgio#2024@host.docker.internal:5432/jobboard",
)

engine = create_engine(DB_URL, echo=True)

Session = sessionmaker(engine)


def clear_db_content() -> None:
    logging.info("Clearing database content.")
    with Session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()


def loading_employers() -> None:
    logging.info("Loading employers data.")
    with Session() as session:
        for employer in employers_data:
            try:
                session.add(Employer(**employer))
            except:
                pass
        session.commit()


def loading_jobs() -> None:
    logging.info("Loading jobs data.")
    with Session() as session:
        for job in jobs_data:
            try:
                session.add(Job(**job))
            except:
                pass
        session.commit()


def prepare_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    loading_employers()
    loading_jobs()


def get_session():
    with Session() as session:
        yield session


def select_all_jobs():
    with Session() as session:
        return session.query(Job).all()


def select_all_employers():
    with Session() as session:
        return session.query(Employer).all()


def select_jobs_for_employer(employer_id: int):
    with Session() as session:
        stmt = select(Job).where(Job.employer_id == employer_id)
        jobs = session.scalars(statement=stmt).all()
        return jobs


def select_employer_for_job(employer_id: int):
    with Session() as session:
        return session.scalars(select(Employer).where(Employer.id == employer_id)).all()
