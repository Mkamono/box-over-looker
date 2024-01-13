from models import Product
from pydantic import BaseModel


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
