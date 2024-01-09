import os
from datetime import datetime

import sqlalchemy
from models import (
    Analysis,
    AnalysisRecord,
    ItemRecord,
    ScrapingResults,
)
from sqlalchemy.orm import Session


def create_session(db_name: str, driver: str = "postgres") -> Session:
    if driver == "sqlite":
        engine = sqlalchemy.create_engine(f"sqlite:///{db_name}.db")
        return Session(engine)
    if driver == "postgres":
        engine = sqlalchemy.create_engine(
            f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{db_name}"
        )
        return Session(engine)
    raise ValueError("Invalid driver")


def migrate_db(db_name: str) -> None:
    session = create_session(db_name)
    ItemRecord.metadata.create_all(session.get_bind())
    AnalysisRecord.metadata.create_all(session.get_bind())
    session.commit()
    session.close()


def create_item_records(db_name: str, results: ScrapingResults):
    session = create_session(db_name)
    session.add_all([item.to_record() for item in results.scraping_results])
    session.commit()
    session.close()


def create_analysis_records(db_name: str, analysis: list[Analysis]):
    session = create_session(db_name)
    session.add_all([item.to_record() for item in analysis])
    session.commit()
    session.close()


def read_item_records(db_name: str) -> list[ItemRecord]:
    session = create_session(db_name)
    records = session.query(ItemRecord).all()
    session.close()
    return records


def read_analysis_records(db_name: str) -> list[AnalysisRecord]:
    session = create_session(db_name)
    records = session.query(AnalysisRecord).all()
    session.close()
    return records


def read_analysis_by_datetime_range(
    db_name: str, datetime_range: tuple[datetime, datetime]
) -> list[Analysis]:
    """_summary_
    この関数は、引数で指定した期間のAnalysisリストを返します。

    Args:
        db_name (str): DBのサーバー名を指定します

        datetime_range (tuple[datetime, datetime]):検索する期間のdatetimeを指定します。
        datetime_range[0]は期間開始のdatetimeを、datetime_range[1]は期間終了のdatetimeを指定します。


    Returns:
        list[Analysis]:Analysisのリスト
    """
    analysis_list = [record.to_analysis() for record in read_analysis_records(db_name)]
    return [
        analysis
        for analysis in analysis_list
        if datetime_range[0] <= analysis.date <= datetime_range[1]
    ]
