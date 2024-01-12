from models import Product
from pydantic import BaseModel


class ComparedResult(BaseModel):
    """
    このクラスは商品の比較結果と結果の算出に用いた値を保持します。

    Attributes:
        product (Product): 比較対象の商品。
        current_price (float): 現在の商品価格。
        is_exceed_thd (bool): 価格が閾値を超えたかどうかを示すフラグ。
        increase_price_percentage (float): 価格の上昇率。
    """

    product: Product
    current_price: float
    is_exceed_thd: bool
    increase_price_percentage: float
