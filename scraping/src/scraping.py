from typing import Callable

from domain.amazon import get_items as get_items_amazon
from domain.mercari import get_items as get_items_mercari
from domain.paypay import get_items as get_items_paypay
from domain.rakuma import get_items as get_items_rakuma
from domain.rakuten import get_items as get_items_rakuten
from domain.yahoo import get_items as get_items_yahoo
from domain.yshop import get_items as get_items_yshop
from errors import ItemNotFoundError
from models import Item, Product
from url import URL
from webdriver import Driver, make_driver


def scraping_all_site(product: Product) -> list[Item]:
    driver = make_driver()

    def get_items_all_pages(
        get_item_from_page: Callable[[Driver, str], list[Item]],
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
    Item_list += get_items_all_pages(get_items_yahoo, url.yahoo)
    print("yahoo取得完了")
    Item_list += get_items_all_pages(get_items_yshop, url.yshop)
    print("yshop取得完了")

    driver.quit()

    return Item_list
