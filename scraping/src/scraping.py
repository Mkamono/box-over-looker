from typing import Callable

from domain.mercari import get_items as get_items_mercari
from domain.paypay import get_items as get_items_paypay
from domain.rakuma import get_items as get_items_rakuma
from errors import ItemNotFoundError
from models import Item, Product
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from url import URL


def setting_driver():
    # ドライバの設定
    options = ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--enable-automation")
    options.add_argument("--headless")  # モニタリングなし
    options.page_load_strategy = "eager"  #  読み込み省略(画像省略)
    service = ChromeService("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scraping_all_site(product: Product) -> list[Item]:
    driver = setting_driver()

    def get_items_all_pages(
        get_item_from_page: Callable[[webdriver.Chrome, str], list[Item]],
        generate_url: Callable[[int], str],
    ) -> list[Item]:
        Item_list: list[Item] = []
        page = 1
        while True:
            try:
                Item_list += get_item_from_page(driver, generate_url(page))
            except ItemNotFoundError:
                break
            page += 1
        return Item_list

    url = URL(product)
    Item_list: list[Item] = []
    Item_list += get_items_all_pages(get_items_rakuma, url.rakuma)
    return Item_list
