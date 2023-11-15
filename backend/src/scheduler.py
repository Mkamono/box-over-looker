import os
from time import sleep

import requests
import schedule

from db import create_item_records
from models import ScrapingResults


def create_scraping_results() -> None:
    scraping_host = os.environ["SCRAPING_HOST"]
    response = requests.get(f"{scraping_host}/scraping")

    scraping_results = ScrapingResults(**response.json())
    create_item_records(db_name="items", results=scraping_results)
    return


def exec_regularly() -> None:
    schedule.every().hour.do(create_scraping_results)
    while True:
        schedule.run_pending()
        sleep(1 * 60)
