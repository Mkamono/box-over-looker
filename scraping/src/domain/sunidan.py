from domain.tools import retry_get_element, retry_get_request
from models import Item, Product, Site
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def login(driver: webdriver.Chrome) -> None:
    url_login = "https://snkrdunk.com/accounts/login/"
    driver.get(url_login)

    @retry_get_element
    def get_login_elem() -> tuple[WebElement, WebElement, WebElement]:
        username_input = driver.find_element(
            By.XPATH, "/html/body/div[2]/section/form/ul/li[1]/input"
        )
        password_input = driver.find_element(
            By.XPATH, "/html/body/div[2]/section/form/ul/li[2]/input"
        )
        submit_button = driver.find_element(
            By.XPATH, "/html/body/div[2]/section/form/button"
        )
        return username_input, password_input, submit_button

    username_input, password_input, submit_button = get_login_elem()

    username_input.send_keys("kakerubass04ls@gmail.com")
    password_input.send_keys("kamono114514")

    submit_button.submit()


@retry_get_request
def get_items(driver: webdriver.Chrome, url: str, product: Product) -> list[Item]:
    login(driver)

    driver.get(url)

    @retry_get_element
    def get_item_grid_elem() -> WebElement:
        return driver.find_element(By.XPATH, "/html/body/div[3]/div/ul")

    item_grid_elem = get_item_grid_elem()

    @retry_get_element
    def get_item_price_list() -> list[int]:
        item_prices = [
            int(e.text.replace(",", "").replace("\u00A5", ""))
            for e in item_grid_elem.find_elements(By.XPATH, "./li/a/div/div[1]/p[1]")
        ]
        return item_prices

    items = [
        Item(title=product.name, price=price, site=Site.スニーカーダンク)
        for price in get_item_price_list()
    ]
    return items
