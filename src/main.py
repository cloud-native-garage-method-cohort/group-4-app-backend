import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

description = """
DFaaS - Dog Facts as a Service 🐕
The one place for all your dogs related facts!
"""

tags_metadata = [
    {
        "name": "fact",
        "description": "Retrieve **one** dog fact at random.",
    },
    {
        "name": "facts",
        "description": "Retrieve **all** of our dog facts",
    },
    {
        "name": "add_fact",
        "description": "Add a dog fact of your **own**!",
    }
]

app = FastAPI(
    title="DFaaS",
    description=description,
    version="0.0.1",
    openapi_tags=tags_metadata)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


db_config = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'woof',
    'host': 'dog-facts-db',
    'port': '5432',
}


class Fact(BaseModel):
    string: str


@app.get("/")
async def check_db(status_code=200):
    try:
        psycopg2.connect(**db_config)
        return 'Wecome to DFaaS See /redoc for Details'
    except Exception as e:
        return 500, repr(e)


@app.post("/add_fact/", status_code=201, tags=["add_fact"])
async def add_fact(fact: Fact):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO dog_facts(fact) VALUES (%s)", (fact.string,))
    conn.commit()
    return 'Fact Added'


@app.get("/fact", tags=["fact"])
async def get_fact():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT fact from dog_facts ORDER BY random() LIMIT 1")
    result = cur.fetchone()
    cur.close()
    return result


@app.get("/facts", tags=["facts"])
async def get_facts():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, fact FROM dog_facts")
    result = cur.fetchall()
    cur.close()
    return result
