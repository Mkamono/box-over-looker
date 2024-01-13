from datetime import datetime, timedelta

from calc import calc_average_median_price, get_current_median_price
from db import RangeDatetime
from env_config import EnvConfig
from models import BaseModel, Product


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


def make_compared_result_list(env_config: EnvConfig) -> list[ComparedResult]:
    db_name: str = "items"  # DBのitemsサーバーを指定
    compared_result_list: list[ComparedResult] = []

    for product in Product:
        current_price = get_current_median_price(
            db_name=db_name,
            product=product,
        )

        average_price = calc_average_median_price(
            db_name=db_name,
            product=product,
            datetime_range=RangeDatetime(
                new=datetime.now(),
                old=datetime.now() - timedelta(days=env_config.period_days),
            ),
        )

        increase_price_percentage: float = (
            (current_price - average_price) / average_price
        ) * 100

        if (increase_price_percentage) > env_config.threshold_increase_rate_price:
            is_exceed_thd = True
        else:
            is_exceed_thd = False

        compared_result_list += [
            ComparedResult(
                product=product,
                current_price=current_price,
                is_exceed_thd=is_exceed_thd,
                increase_price_percentage=increase_price_percentage,
            )
        ]
    return compared_result_list
