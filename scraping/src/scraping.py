from typing import Callable

from domain.amazon import get_items as get_items_amazon
from domain.mercari import get_items as get_items_mercari
from domain.paypay import get_items as get_items_paypay
from domain.rakuma import get_items as get_items_rakuma
from domain.rakuten import get_items as get_items_rakuten
from domain.sunidan import get_items as get_items_sunidan
from domain.yahoo import get_items as get_items_yahoo
from domain.yshop import get_items as get_items_yshop
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
            except Exception as e:
                print("予期せぬエラーが発生しました。")
                print(e)
                break
            page += 1
        return Item_list

    url = URL(product)
    Item_list: list[Item] = []
    Item_list += get_items_all_pages(get_items_amazon, url.amazon)
    print("amazon取得完了")
    Item_list += get_items_all_pages(get_items_mercari, url.mercari)
    print("mercari取得完了")
    Item_list += get_items_all_pages(get_items_paypay, url.paypay)
    print("paypay取得完了")
    Item_list += get_items_all_pages(get_items_rakuma, url.rakuma)
    print("rakuma取得完了")
    Item_list += get_items_all_pages(get_items_rakuten, url.rakuten)
    print("rakuten取得完了")
    Item_list += get_items_sunidan(driver, url.sunidan(), product)
    print("sunidan取得完了")
    Item_list += get_items_all_pages(get_items_yahoo, url.yahoo)
    print("yahoo取得完了")
    Item_list += get_items_all_pages(get_items_yshop, url.yshop)
    print("yshop取得完了")

    driver.quit()

    return Item_list
