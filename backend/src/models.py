import os
from datetime import datetime
from enum import StrEnum

import requests
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Enum, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Mail(BaseModel):
    title: str
    user_address: str
    body: str

    def post_mail(self) -> None:
        mail_host = os.environ.get("MAIL_HOST")
        if mail_host is None:
            raise ValueError("MAIL_HOST environment variable is not set.")
        try:
            requests.post(f"{mail_host}/send_mail", json=self.model_dump_json())
        except Exception as e:
            print("Failed to send Email because of following error.")
            print(e)


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


class Analysis(BaseModel):
    ID: str = ""
    product: Product
    median: float
    date: datetime

    def to_record(self):
        return AnalysisRecord(
            ID=self.ID,
            date=str(self.date),
            median=self.median,
            product=self.product.name,
        )


class AnalysisRecord(Base):
    __tablename__ = "analysis"
    ID = Column(String, primary_key=True)
    date = Column(DateTime, nullable=False)
    median = Column(Float, nullable=False)
    product = Column(Enum(Product), nullable=False)

    def format_via_str(self, value, target_type: type):
        return target_type(str(value))

    def to_analysis(self):
        return Analysis(
            ID=self.format_via_str(self.ID, str),
            date=datetime.strptime(str(self.date), "%Y-%m-%d %H:%M:%S.%f"),
            median=self.format_via_str(self.median, float),
            product=Product[self.product.name],
        )
