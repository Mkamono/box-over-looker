import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from domain.tools import retry
from errors import ItemNotFoundError
from models import Item, Site


def check_status_code(url: str):
    res = requests.get(url)
    if res.status_code == 200:
        return
    if res.status_code == 404:
        raise ItemNotFoundError
    res.raise_for_status()
    raise Exception("レスポンスエラー")


def get_items(driver: webdriver.Chrome, url: str) -> list[Item]:
    driver.get(url)
    check_status_code(url)

    @retry
    def get_item_grid_elem() -> WebElement:
        return driver.find_element(
            By.XPATH,
            "/html/body/div[3]/div/div/div/div/div/div[2]/section/div[2]/section",
        )

    item_grid_elem = get_item_grid_elem()

    @retry
    def get_item_info_list() -> tuple[list[str], list[int]]:
        item_titles = [
            str(e.get_attribute("alt")).replace("　", " ")
            for e in item_grid_elem.find_elements(By.XPATH, "./div/div/div[1]/a/img")
        ]
        item_prices = [
            int(e.text.replace(",", "").replace("円", ""))
            for e in item_grid_elem.find_elements(
                By.XPATH, "./div/div/div[2]/div[2]/div[1]/p/span[2]"
            )
        ]
        return item_titles, item_prices

    items = [
        Item(title=title, price=price, site=Site.楽天ラクマ)
        for title, price in zip(*get_item_info_list())
    ]

    return items
