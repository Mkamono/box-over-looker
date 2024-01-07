import os
from multiprocessing import Process
from time import sleep

from migrate import migrate_db
from scheduler import exec_regularly
from server import run_server


def run_parallel_process() -> None:
    server_process = Process(target=run_server)
    schedule_process = Process(target=exec_regularly)

    server_process.start()
    schedule_process.start()

    server_process.join()
    schedule_process.join()


if __name__ == "__main__":
    sleep(5)
    migrate_db(db_name=os.environ["POSTGRES_DB"])
    run_parallel_process()
