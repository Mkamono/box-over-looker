from db import migrate_db
import os


if __name__ == "__main__":
    migrate_db(db_name=os.environ["POSTGRES_DB"])
