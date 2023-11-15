from uuid import uuid4

import sqlalchemy
from models import ItemRecord, ScrapingResults
from sqlalchemy.orm import Session


def create_session(db_name: str) -> Session:
    engine = sqlalchemy.create_engine(f"postgresql://kakeru:bol@db/{db_name}")
    return Session(engine)


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
