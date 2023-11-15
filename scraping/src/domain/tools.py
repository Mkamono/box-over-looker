from time import sleep

from errors import ItemNotFoundError


def retry(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except ItemNotFoundError as e:
                raise e
            except:
                sleep(1)

    return wrapper
