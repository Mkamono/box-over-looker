import os
from time import sleep

import requests
import schedule
from calc import make_analysis_list
from db import create_analysis_records, create_item_records
from mail import make_compared_result_list, make_mail_class
from models import ScrapingResults
from user_config import get_user_config


# SCからレスポンスを受け取り次第、2つのテーブルに格納させる
def make_records() -> None:
    response = requests.get(
        f"http://{os.environ['SCRAPING_HOST']}:{os.environ['SCRAPING_PORT']}/scraping"
    )
    scraping_results = ScrapingResults(**response.json())
    create_item_records(db_name=os.environ["POSTGRES_DB"], results=scraping_results)
    create_analysis_records(
        db_name=os.environ["POSTGRES_DB"], analysis=make_analysis_list(scraping_results)
    )


# メール関連の演算はDBのREADから処理を行うため、SCのレスポンスに関係しない
def send_mail() -> None:
    make_compared_results = make_compared_result_list()
    mail = make_mail_class(make_compared_results)
    mail.post_mail()


# compose upするときに実行されるため、ユーザー設定をその時に読み込む
# 読み込んだ結果を用いてスケジューラーに登録する
# 通知頻度のユーザー設定を変更した時は、コンテナを再起動する必要がある
def exec_regularly() -> None:
    schedule.every().hour.at(":00").do(make_records)

    user_config = get_user_config()

    if user_config.notification_timing.zero:
        schedule.every().day.at("00:00").do(send_mail)
    if user_config.notification_timing.six:
        schedule.every().day.at("06:00").do(send_mail)
    if user_config.notification_timing.twelve:
        schedule.every().day.at("12:00").do(send_mail)
    if user_config.notification_timing.eighteen:
        schedule.every().day.at("18:00").do(send_mail)

    while True:
        schedule.run_pending()
        sleep(1 * 60)
