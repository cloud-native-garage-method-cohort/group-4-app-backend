import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

description = """
## **DFaaS** - I’m **D**og **F**acts **a**s **a** **S**ervice 🐕  <br />
The one place for all your dogs related facts!
"""

app = FastAPI(
    title="DFaaS",
    description=description,
    version="0.0.1")

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


@app.get("/")
async def check_db(status_code=200):
    try:
        psycopg2.connect(**db_config)
        return 'Wecome to DFaaS See /redoc for Details'
    except Exception as e:
        return 500, repr(e)


@app.post("/add_fact/", status_code=201)
async def add_fact(fact: str):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO dog_facts(fact) VALUES (%s)", (fact,))
    conn.commit()
    return 'Fact Added'


@app.get("/fact")
async def get_fact():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT fact from dog_facts ORDER BY random() LIMIT 1")
    result = cur.fetchone()
    cur.close()
    return result


@app.get("/facts")
async def get_facts():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, fact FROM dog_facts")
    result = cur.fetchall()
    cur.close()
    return result
