from graphene import Schema, ObjectType, List
from sqlalchemy.orm import joinedload

from app.gql.type import JobObject, EmployerObject
from app.db.models import Job, Employer
from app.db.database import select_all_employers, select_all_jobs, Session


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        with Session() as session:
            return session.query(Job).options(joinedload(Job.employer)).all()

    @staticmethod
    def resolve_employers(root, info):
        with Session() as session:
            return session.query(Employer).options(joinedload(Employer.jobs)).all()


schema = Schema(query=Query)
