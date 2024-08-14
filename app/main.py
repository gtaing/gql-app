from graphene import Schema, ObjectType, List
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler


from app.entity import JobObject, EmployerObject
from app.database import loading_data
from app.data import jobs_data, employers_data


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        return jobs_data

    @staticmethod
    def resolve_employers(root, info):
        return employers_data


schema = Schema(query=Query)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_playground_handler()))


# Loading data into DB
loading_data()
