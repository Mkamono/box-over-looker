from re import S
from uuid import uuid4

from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import ItemRecord, ScrapingResults


def create_session(db_name: str):
    engine = create_engine(f"postgresql://kakeru:bol@localhost/{db_name}")
    Session = sessionmaker(bind=engine)
    return Session()


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
