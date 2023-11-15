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
    scraping_host = os.environ["SCRAPING_HOST"]
    response = requests.get(f"{scraping_host}/scraping").json()

    scraping_results = ScrapingResults(**response)
    create_item_records(db_name="items", results=scraping_results)
    return scraping_results


def run_server() -> None:
    uvicorn.run(app, port=int(os.environ["BACKEND_PORT"]))


if __name__ == "__main__":
    run_server()
