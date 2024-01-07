from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class Site(StrEnum):
    メルカリ = "メルカリ"
    Paypayフリマ = "Paypayフリマ"
    楽天ラクマ = "楽天ラクマ"
    ヤフオク = "ヤフオク"
    スニーカーダンク = "スニーカーダンク"
    amazon = "amazon"
    楽天市場 = "楽天市場"
    ヤフーショッピング = "ヤフーショッピング"


class Product(StrEnum):
    ポケモンカード151 = "ポケモンカード151"
    黒炎の支配者 = "黒炎の支配者"
    レイジングサーフ = "レイジングサーフ"


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
