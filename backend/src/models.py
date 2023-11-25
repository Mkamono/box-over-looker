import os
from datetime import datetime
from enum import IntEnum

import requests
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Mail(BaseModel):
    title: str
    user_address: str
    body: str

    def post_mail(self) -> None:
        requests.post(f"{os.environ['MAIL_HOST']}/send_mail", json=self)


class Site(IntEnum):
    メルカリ = 1
    Paypayフリマ = 2
    楽天ラクマ = 3
    ヤフオク = 4
    スニーカーダンク = 5
    amazon = 6
    楽天市場 = 7
    ヤフーショッピング = 8


class Product(IntEnum):
    ポケモンカード151 = 1
    黒炎の支配者 = 2
    レイジングサーフ = 3


class Base(DeclarativeBase):
    pass


class Item(BaseModel):
    title: str
    price: int
    site: Site


class ScrapingResult(BaseModel):
    ID: str = ""
    date: datetime
    Item: Item
    product: Product

    def to_record(self):
        return ItemRecord(
            ID=self.ID,
            date=str(self.date),
            title=self.Item.title,
            price=self.Item.price,
            site=self.Item.site.name,
            product=self.product.name,
        )


class ScrapingResults(BaseModel):
    scraping_results: list[ScrapingResult]


class ItemRecord(Base):
    __tablename__ = "items"
    ID = Column(String, primary_key=True)
    date = Column(String, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    site = Column(String, nullable=False)
    product = Column(String, nullable=False)

    def format_via_str(self, value, target_type: type):
        return target_type(str(value))

    def format_to_site(self, site_name: Column) -> Site:
        for site in Site:
            if str(site_name) == site.name:
                return site
        else:
            raise ValueError(f"site_name: {site_name} is not in Site.")

    def format_to_product(self, product_name: Column) -> Product:
        for product in Product:
            if str(product_name) == product.name:
                return product
        else:
            raise ValueError(f"product_name: {product_name} is not in Product.")

    def format_to_datetime(self, date: Column) -> datetime:
        return datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S.%f")

    def to_scraping_result(self):
        return ScrapingResult(
            ID=self.format_via_str(self.ID, str),
            date=self.format_to_datetime(self.date),
            Item=Item(
                title=self.format_via_str(self.title, str),
                price=self.format_via_str(self.price, int),
                site=self.format_to_site(self.site),
            ),
            product=self.format_to_product(self.product),
        )
