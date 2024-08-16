from typing import Annotated
from graphene import Schema
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from starlette_graphene3 import GraphQLApp, make_playground_handler

from app.db.database import prepare_db, get_session
from app.db.models import Employer, Job
from app.gql.query import Query
from app.gql.mutation import Mutation


@asynccontextmanager
async def lifespan(app: FastAPI):
    prepare_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/employers")
async def get_employers(session: Annotated[None, Depends(get_session)]):
    return session.query(Employer).all()


@app.get("/jobs")
async def get_jobs(session: Annotated[None, Depends(get_session)]):
    return session.query(Job).all()


schema = Schema(query=Query, mutation=Mutation)

app.mount("/graphql", GraphQLApp(schema=schema, on_get=make_playground_handler()))
