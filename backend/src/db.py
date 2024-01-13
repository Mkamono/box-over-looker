import os
from datetime import datetime

import sqlalchemy
from error import NoRecordError
from models import Analysis, AnalysisRecord, ItemRecord, Product, ScrapingResults
from pydantic import BaseModel
from sqlalchemy import and_
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


class RangeDatetime(BaseModel):
    new: datetime
    old: datetime


def read_analysis_by_datetime(db_name: str, datetime_range: RangeDatetime):
    session = create_session(db_name)
    records = (
        session.query(AnalysisRecord)
        .filter(
            and_(
                AnalysisRecord.date >= datetime_range.old,
                AnalysisRecord.date <= datetime_range.new,
            )
        )
        .all()
    )
    session.close()
    return records


def read_latest_analysis_record(db_name: str, product: Product) -> AnalysisRecord:
    session = create_session(db_name)
    record = (
        session.query(AnalysisRecord)
        .order_by(AnalysisRecord.date.desc())
        .filter(AnalysisRecord.product == product)
        .first()
    )
    session.close()
    if record is None:
        raise NoRecordError("No record found")
    return record
