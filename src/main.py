import psycopg2
import requests
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor


app = FastAPI()


db_config = {
    'database': 'postgres',
    'user': 'postgres',
    'password': 'woof',
    'host': 'dog-facts-db',
    'port': '5432',
}


@app.get("/")
async def get_fact():
    url = 'https://dog-api.kinduff.com/api/facts'
    data = {'number': 1}
    response = requests.get(url, data).json()['facts'][0]
    
    return {"fact": response}


@app.get("/check_db")
async def check_db():
    try:
        con = psycopg2.connect(**db_config)
        return "Database opened successfully"
    except Exception as e:
        return repr(e)


@app.get("/get_all_facts")
async def get_all_facts():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    query_sql = "SELECT id, fact FROM dog_facts" 
    cur.execute(query_sql)
    results = cur.fetchall()
    return results