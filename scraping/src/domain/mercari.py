from errors import ItemNotFoundError
from models import Item, Site
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from domain.tools import retry_get_element, retry_get_request


def check_item_not_found(driver: webdriver.Remote):
    def get_elem_not_found() -> WebElement:
        not_found_elem = driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/div[2]/main/div/div/div/div/div/section[2]/div/div/div[1]/p",
        )
        return not_found_elem

    try:
        get_elem_not_found()
    except NoSuchElementException:
        return
    raise ItemNotFoundError


@retry_get_request
def get_items(driver: webdriver.Remote, url: str) -> list[Item]:
    driver.get(url)

    @retry_get_element
    def get_item_grid_elem() -> WebElement:
        check_item_not_found(driver)
        item_grid_elem = driver.find_element(By.ID, "item-grid")
        return item_grid_elem

    item_grid_elem = get_item_grid_elem()

    @retry_get_element
    def get_item_info_list() -> tuple[list[str], list[int]]:
        item_base = "./ul/li/div/a/div/figure"
        item_titles = [
            str(e.get_attribute("alt")).replace("　", " ")[:-6]
            for e in item_grid_elem.find_elements(
                By.XPATH, f"{item_base}/div[2]/picture/img"
            )
        ]
        item_prices = [
            int(e.text.replace(",", ""))
            for e in item_grid_elem.find_elements(
                By.XPATH, f"{item_base}/div[3]/div/span/span[2]"
            )
        ]
        return item_titles, item_prices

    items = [
        Item(title=title, price=price, site=Site.メルカリ)
        for title, price in zip(*get_item_info_list())
    ]
    return items
