import os
from time import sleep

import requests
import schedule
from db import create_item_records
from models import ScrapingResults


def create_scraping_results() -> None:
    response = requests.get(
        f"http://{os.environ['SCRAPING_HOST']}:{os.environ['SCRAPING_PORT']}/scraping"
    )
    scraping_results = ScrapingResults(**response.json())
    create_item_records(db_name=os.environ["POSTGRES_DB"], results=scraping_results)
    return


def exec_regularly() -> None:
    schedule.every().hour.do(create_scraping_results)
    while True:
        schedule.run_pending()
        sleep(1 * 60)
