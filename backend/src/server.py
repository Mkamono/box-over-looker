import os

import requests
import uvicorn
from fastapi import FastAPI

from db import create_item_records
from models import ScrapingResults

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/dev/create/results")
async def create_results():
    response = requests.get(
        f"http://{os.environ['SCRAPING_HOST']}:{os.environ['SCRAPING_PORT']}/scraping"
    ).json()
    scraping_results = ScrapingResults(**response)
    create_item_records(db_name=os.environ["POSTGRES_DB"], results=scraping_results)
    return scraping_results


def run_server() -> None:
    uvicorn.run(app, port=int(os.environ["BACKEND_PORT"]), host="0.0.0.0")


if __name__ == "__main__":
    run_server()
