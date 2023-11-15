from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel


class Product(IntEnum):
    ポケモンカード151 = 1
    黒炎の支配者 = 2
    レイジングサーフ = 3


class Site(IntEnum):
    メルカリ = 1
    Paypayフリマ = 2
    楽天ラクマ = 3
    ヤフオク = 4
    スニーカーダンク = 5
    amazon = 6
    楽天市場 = 7
    ヤフーショッピング = 8


class Item(BaseModel):
    title: str
    price: int
    site: Site


class ScrapingResult(BaseModel):
    date: datetime
    Item: Item
    product: Product


class ScrapingResults(BaseModel):
    scraping_results: list[ScrapingResult]
