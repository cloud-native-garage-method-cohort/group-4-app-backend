import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


db_config = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'woof',
    'host': 'dog-facts-db',
    'port': '5432',
}

class Fact(BaseModel):
    string: str


@app.post("/add_fact/")
async def add_fact(fact: Fact):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO dog_facts(fact) VALUES (%s)", (fact,))
    conn.commit()
    cur.close()
    return 'Fact Added'


@app.get("/fact")
async def get_fact():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT fact from dog_facts ORDER BY random() LIMIT 1")
    cur.close()
    return cur.fetchone()


@app.get("/facts")
async def get_facts():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, fact FROM dog_facts")
    cur.close()
    return cur.fetchall()
