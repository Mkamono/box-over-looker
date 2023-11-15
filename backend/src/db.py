import os
from uuid import uuid4

import sqlalchemy
from models import ItemRecord, ScrapingResults
from sqlalchemy.orm import Session


def create_session(db_name: str, driver: str = "postgres") -> Session:
    if driver == "sqlite":
        engine = sqlalchemy.create_engine(f"sqlite:///{db_name}.db")
        return Session(engine)
    if driver == "postgres":
        engine = sqlalchemy.create_engine(
            f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{db_name}"
        )
        return Session(engine)
    raise ValueError("Invalid driver")


def migrate_db(db_name: str):
    session = create_session(db_name)
    ItemRecord.metadata.create_all(session.get_bind())
    session.commit()
    session.close()


def create_item_records(db_name: str, results: ScrapingResults):
    session = create_session(db_name)
    for item in results.scraping_results:
        item.ID = str(uuid4())

    session.add_all([item.to_record() for item in results.scraping_results])

    session.commit()
    session.close()
