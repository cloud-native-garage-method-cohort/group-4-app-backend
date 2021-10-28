from fastapi import FastAPI
import requests
import psycopg2


app = FastAPI()

@app.get("/")
async def get_fact():
    url = 'https://dog-api.kinduff.com/api/facts'
    data = {'number': 1}
    response = requests.get(url, data).json()['facts'][0]
    
    return {"fact": response}

@app.get("/check_db")
async def check_db():
    try:
        con = psycopg2.connect(database="dog-facts-db", user="postgres", password="woof", host="dog-facts-db", port="5432")
        print("Database opened successfully")
    except Exception as e:
        print(repr(e))