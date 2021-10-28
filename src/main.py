from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
async def get_fact():
    url = 'https://dog-api.kinduff.com/api/facts'
    data = {'number': 1}
    response = requests.get(url, data).json()['facts'][0]
    
    return {"fact": response}
