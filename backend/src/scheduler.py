import os
from datetime import datetime
from time import sleep

import requests
import schedule
from calc import make_analysis_list
from db import create_analysis_records, create_item_records
from mail import make_compared_result_list, make_mail_class
from models import ScrapingResults
from user_config import get_user_config


def create_item_and_analysis_records() -> None:
    response = requests.get(
        f"http://{os.environ['SCRAPING_HOST']}:{os.environ['SCRAPING_PORT']}/scraping"
    )
    scraping_results = ScrapingResults(**response.json())
    create_item_records(db_name=os.environ["POSTGRES_DB"], results=scraping_results)
    create_analysis_records(
        db_name=os.environ["POSTGRES_DB"], analysis=make_analysis_list(scraping_results)
    )


def send_mail() -> None:
    compared_results = make_compared_result_list()
    mail = make_mail_class(compared_results)
    mail.post_mail()


def send_mail_based_user_config() -> None:
    user_config = get_user_config()
    current_hour = datetime.now().hour

    if user_config.notification_timing.zero & current_hour == 0:
        send_mail()
    if user_config.notification_timing.six & current_hour == 6:
        send_mail()
    if user_config.notification_timing.twelve & current_hour == 12:
        send_mail()
    if user_config.notification_timing.eighteen & current_hour == 18:
        send_mail()


def exec_regularly() -> None:
    schedule.every().hour.at(":00").do(create_item_and_analysis_records)
    schedule.every().hour.at(":00").do(send_mail_based_user_config)

    while True:
        schedule.run_pending()
        sleep(1 * 60)
