import os

from db import migrate_db

if __name__ == "__main__":
    migrate_db(db_name=os.environ["POSTGRES_DB"])
