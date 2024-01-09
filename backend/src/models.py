import os
from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID as uuid
from uuid import uuid4

import requests
from pydantic import BaseModel, ConfigDict
from sqlalchemy import UUID, Column, DateTime, Enum, Float, Integer, String
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
    model_config = ConfigDict(from_attributes=True)

    ID: Optional[uuid] = None
    date: datetime
    product: Product

    item: Optional[Item] = None
    title: Optional[str] = None
    price: Optional[int] = None
    site: Optional[Site] = None

    def fill_item(self) -> None:
        # self.itemまたはtitle, price, siteのどちらか存在している方を採用する
        if self.item is None:
            if self.title is None or self.price is None or self.site is None:
                raise ValueError("item or title, price, site must be set.")
            self.item = Item(
                title=self.title,
                price=self.price,
                site=self.site,
            )

        if any(
            [
                self.title is None,
                self.price is None,
                self.site is None,
            ]
        ):
            self.title = self.item.title
            self.price = self.item.price
            self.site = self.item.site

    def model_post_init(self, __context) -> None:
        if self.ID is None:
            self.ID = uuid4()

        self.fill_item()

    def to_record(self):
        return ItemRecord(
            ID=self.ID,
            date=self.date,
            title=self.title,
            price=self.price,
            site=self.site,
            product=self.product,
        )


class ScrapingResults(BaseModel):
    scraping_results: list[ScrapingResult]


class ItemRecord(Base):
    __tablename__ = "items"
    ID = Column(UUID, primary_key=True)
    date = Column(DateTime, nullable=False)
    product = Column(Enum(Product), nullable=False)

    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    site = Column(Enum(Site), nullable=False)

    def to_scraping_result(self):
        return ScrapingResult.model_validate(self)


class Analysis(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: Optional[uuid] = None
    product: Product
    median: float
    date: datetime

    def model_post_init(self, __context) -> None:
        if self.ID is None:
            self.ID = uuid4()

    def to_record(self):
        return AnalysisRecord(
            ID=self.ID,
            date=self.date,
            median=self.median,
            product=self.product,
        )


class AnalysisRecord(Base):
    __tablename__ = "analysis"
    ID = Column(UUID, primary_key=True)
    date = Column(DateTime, nullable=False)
    median = Column(Float, nullable=False)
    product = Column(Enum(Product), nullable=False)

    def to_analysis(self):
        return Analysis.model_validate(self)


class RangeDatetime(BaseModel):
    new: datetime
    old: datetime
