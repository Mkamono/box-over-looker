from datetime import datetime, timedelta

from calc import calc_average_median_price, get_current_median_price
from db import RangeDatetime
from models import Product
from pydantic import BaseModel
from user_config import UserConfig, get_user_config


class ComparedResult(BaseModel):
    """
    過去データとの比較結果を表すクラス。

    Attributes:
        product (Product): 比較対象の商品。
        current_price (float): 直近のスクレイピング結果における、価格の中央値。
        is_exceed_thd (bool): 価格が閾値を超えたかどうかを示すフラグ。
        increase_price_percentage (float): 価格の上昇率。
    """

    product: Product
    current_price: float
    is_exceed_thd: bool
    increase_price_percentage: float


def make_compared_result_list() -> list[ComparedResult]:
    db_name: str = "items"  # itemsデータベースを指定
    user_config = get_user_config()  # ユーザー設定の環境変数を読み込む

    def make_compared_result(
        product: Product, db_name: str, user_config: UserConfig
    ) -> ComparedResult:
        current_price = get_current_median_price(
            db_name=db_name,
            product=product,
        )

        average_price = calc_average_median_price(
            db_name=db_name,
            product=product,
            datetime_range=RangeDatetime(
                new=datetime.now(),
                old=datetime.now() - timedelta(days=user_config.period_days),
            ),
        )

        if average_price != 0:
            increase_price_percentage = (
                (current_price - average_price) / average_price
            ) * 100
        else:
            increase_price_percentage = 0.0

        is_exceed_thd = (
            increase_price_percentage > user_config.threshold_increase_rate_price
        )

        return ComparedResult(
            product=product,
            current_price=current_price,
            is_exceed_thd=is_exceed_thd,
            increase_price_percentage=increase_price_percentage,
        )

    compared_result_list: list[ComparedResult] = [
        make_compared_result(product, db_name, user_config) for product in Product
    ]
    return compared_result_list


def make_mail_title(compared_results: list[ComparedResult]) -> str:
    # 閾値を超えた商品のリストを作成
    products_exceed_thd: list[Product] = [
        compared_result.product
        for compared_result in compared_results
        if compared_result.is_exceed_thd
    ]

    # メールのタイトルを作成
    if products_exceed_thd:
        return f"【お知らせ】{ ', '.join([product for product in products_exceed_thd])}で急激な価格の上昇がありました。"
    return "【お知らせ】急激な価格の上昇はありませんでした。"
