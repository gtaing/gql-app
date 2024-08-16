from graphene import Mutation, ObjectType
from graphene import String, Int, Field
from sqlalchemy import insert, update

from app.gql.type import JobObject, EmployerObject
from app.db.database import Session
from app.db.models import Job, Employer


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        with Session() as session:
            session.execute(
                insert(Employer).values(
                    name=name, contact_email=contact_email, industry=industry
                )
            )

            session.commit()

        return AddEmployer(
            Employer(name=name, contact_email=contact_email, industry=industry)
        )


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        with Session() as session:
            session.execute(
                insert(Job).values(
                    title=title, description=description, employer_id=employer_id
                )
            )

            session.commit()

        return AddJob(
            job=Job(title=title, description=description, employer_id=employer_id)
        )


class UpdateJob(Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, id, title=None, description=None, employer_id=None):

        fields_to_update = {
            k: v
            for k, v in dict(
                [
                    ("title", title),
                    ("description", description),
                    ("employer_id", employer_id),
                ]
            ).items()
            if v is not None
        }

        print(fields_to_update)

        with Session() as session:

            if not session.query(Job).filter(Job.id == id).first():
                raise Exception("Job not found.")

            session.execute(update(Job).where(Job.id == id).values(**fields_to_update))
            session.commit()

        return UpdateJob(job=session.query(Job).filter(Job.id == id).first())


class UpdateEmployer(Mutation):
    class Arguments:
        employer_id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, employer_id, name=None, contact_email=None, industry=None):

        with Session() as session:

            employer_to_update = (
                session.query(Employer).filter(Employer.id == employer_id).first()
            )

            if not employer_to_update:
                raise Exception("Employer not found.")

            if name:
                employer_to_update.name = name
            if contact_email:
                employer_to_update.contact_email = contact_email
            if industry:
                employer_to_update.industry = industry

            session.commit()
            session.refresh(employer_to_update)

        return UpdateEmployer(employer=employer_to_update)


class Mutation(ObjectType):
    add_job = AddJob.Field()
    add_employer = AddEmployer.Field()

    update_job = UpdateJob.Field()
    update_employer = UpdateEmployer.Field()
