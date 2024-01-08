import datetime
import os

import uvicorn
from fastapi import FastAPI
from models import Item, Product, ScrapingResult, ScrapingResults, Site
from scraping import scraping_all_site

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/scraping")
def get_ScrapingResults() -> ScrapingResults:
    scraping_results: list[ScrapingResult] = []

    for product in Product:
        items = [
            ScrapingResult(date=datetime.datetime.now(), item=item, product=product)
            for item in scraping_all_site(product)
        ]
        scraping_results += items

    return ScrapingResults(scraping_results=scraping_results)


# 開発用モックエンドポイント
@app.get("/scraping_mock")
def get_ScrapingResults_mock() -> ScrapingResults:
    return ScrapingResults(
        scraping_results=[
            ScrapingResult(
                date=datetime.datetime.now(),
                item=Item(title="mock_1", price=5000, site=Site.メルカリ),
                product=Product.ポケモンカード151,
            ),
            ScrapingResult(
                date=datetime.datetime.now(),
                item=Item(title="mock_2", price=6000, site=Site.ヤフオク),
                product=Product.黒炎の支配者,
            ),
        ]
    )


def run_server() -> None:
    uvicorn.run(app, port=int(os.environ["SCRAPING_PORT"]), host="0.0.0.0")


if __name__ == "__main__":
    run_server()
