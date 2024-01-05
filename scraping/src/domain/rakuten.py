from errors import ItemNotFoundError
from models import Item, Site
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from domain.tools import retry_get_element, retry_get_request


def check_item_not_found(driver: webdriver.Remote) -> None:
    def get_elem_not_found() -> WebElement:
        not_found_elem = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div[1]/div[2]/div[1]/h1",
        )
        return not_found_elem

    def get_elem_not_sold() -> WebElement:
        not_sold_elem = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[2]/div/div[5]/div[1]/p",
        )
        return not_sold_elem

    try:
        get_elem_not_found()
    except NoSuchElementException:
        pass
    except Exception as e:
        raise e
    else:
        raise ItemNotFoundError

    try:
        get_elem_not_sold()
    except NoSuchElementException:
        return
    except Exception as e:
        raise e
    else:
        raise ItemNotFoundError


@retry_get_request
def get_items(driver: webdriver.Remote, url: str) -> list[Item]:
    driver.get(url)

    @retry_get_element
    def get_item_grid_elem() -> WebElement:
        check_item_not_found(driver)
        item_grid_elem = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[5]/div"
        )
        return item_grid_elem

    item_grid_elem = get_item_grid_elem()

    @retry_get_element
    def get_item_info_list() -> tuple[list[str], list[int]]:
        item_titles = [
            str(e.text).replace("　", " ")
            for e in item_grid_elem.find_elements(
                By.XPATH, "./div/div/div[1]/div[1]/div/p[1]"
            )
        ]
        item_prices = [
            int(e.text.replace(",", "").replace("\u00A5", ""))
            for e in item_grid_elem.find_elements(
                By.XPATH, "./div/div/div[2]/div/p/span"
            )
        ]
        return item_titles, item_prices

    items = [
        Item(title=title, price=price, site=Site.楽天市場)
        for title, price in zip(*get_item_info_list())
    ]
    return items
