from time import sleep

from errors import IncorrectGetError, ItemNotFoundError


def retry_get_element(func):
    def wrapper(*args, **kwargs):
        for i in range(10):
            try:
                return func(*args, **kwargs)
            except ItemNotFoundError as e:
                raise e
            except:
                sleep(1)
        raise IncorrectGetError

    return wrapper


def retry_get_request(func):
    def wrapper(*args, **kwargs):
        for i in range(3):
            try:
                return func(*args, **kwargs)
            except IncorrectGetError:
                print("GETリクエストに失敗しました。リトライします。")
                continue
            except Exception as e:
                print("GETリクエストに予期せぬエラーが発生しました。")
                print(e)
                raise e
        raise ItemNotFoundError

    return wrapper
