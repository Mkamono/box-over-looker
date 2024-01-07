from errors import ItemNotFoundError
from models import Item, Site
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from webdriver import Driver, WebElement

from domain.tools import retry_get_element, retry_get_request


def check_item_not_found(driver: Driver) -> None:
    def get_elem_not_found() -> WebElement:
        not_found_elem = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div[1]/div/div/main/div/div/div[2]/div[2]/div[1]/div/p/span",
        )
        return not_found_elem

    try:
        get_elem_not_found()
    except NoSuchElementException:
        return
    raise ItemNotFoundError


@retry_get_request
def get_items(driver: Driver, url: str) -> list[Item]:
    driver.get(url)

    @retry_get_element
    def get_item_grid_elem() -> WebElement:
        check_item_not_found(driver)
        item_grid_elem = driver.find_element(By.ID, "itm")
        return item_grid_elem

    item_grid_elem = get_item_grid_elem()

    @retry_get_element
    def get_item_info_list() -> tuple[list[str], list[int]]:
        item_titles = [
            str(e.get_attribute("alt")).replace("　", " ")
            for e in item_grid_elem.find_elements(By.XPATH, "./a/img")
        ]
        item_prices = [
            int(e.text.replace(",", "").replace("円", ""))
            for e in item_grid_elem.find_elements(By.XPATH, "./a/p")
        ]
        return item_titles, item_prices

    items = [
        Item(title=title, price=price, site=Site.Paypayフリマ)
        for title, price in zip(*get_item_info_list())
    ]
    return items
