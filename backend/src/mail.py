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


def make_title(compared_results: list[ComparedResult]) -> str:
    # 閾値を超えた商品のリストを作成
    product_exceed_thd: list[Product] = [
        compared_result.product
        for compared_result in compared_results
        if compared_result.is_exceed_thd
    ]

    # メールのタイトルを作成
    if product_exceed_thd:
        mail_title: str = f"【お知らせ】{ ', '.join([product.name for product in product_exceed_thd])}で急激な価格の上昇がありました。"
    else:
        mail_title: str = "【お知らせ】急激な価格の上昇はありませんでした。"

    return mail_title


def japanize_percentage(percentage: float) -> str:
    suffix = "上昇" if percentage > 0 else "減少"
    return f"{int(abs(percentage))}%" + suffix


def make_mail_body(compared_results: list[ComparedResult]) -> str:
    user_config = get_user_config()

    now_hour = datetime.now().hour

    def make_trading_timing_txt(hour: int):
        return f"本日の{hour}時時点での取引価格によるお知らせです。"

    def make_exceed_txt(compared_results: list[ComparedResult]) -> str:
        if len(compared_results) == 0:
            return ""

        exceed_header = "価格の急激な上昇が確認された商品"

        def make_body(compared_result: ComparedResult) -> str:
            return f"・{compared_result.product}。\n現在の取引価格は約{int(compared_result.current_price)}円です。急激な価格の上昇が起きています。過去{user_config.period_days}日間の平均価格と比較して、{japanize_percentage(compared_result.increase_price_percentage)}しています。"

        exceed_body = "\n\n".join([make_body(c) for c in compared_results])

        return exceed_header + "\n" + exceed_body

    def make_unexceed_txt(compared_results: list[ComparedResult]) -> str:
        if len(compared_results) == 0:
            return ""

        unexceed_header = "価格の急激な上昇が確認されなかった商品"

        def make_body(compared_result: ComparedResult) -> str:
            return f"・{compared_result.product}。\n現在の取引価格は約{int(compared_result.current_price)}円です。過去{user_config.period_days}日間の平均価格と比較して、{japanize_percentage(compared_result.increase_price_percentage)}しています。"

        unexceed_body = "\n\n".join([make_body(c) for c in compared_results])
        return unexceed_header + "\n" + unexceed_body

    footer_txt = (
        f"現在の閾値は{user_config.threshold_increase_rate_price}%です。閾値の変更は、以下のURLのReadmeをお読みください。"
        + "\n"
        + "https://github.com/Mkamono/box-over-looker"
    )

    return "\n\n".join(
        [
            s
            for s in [
                make_trading_timing_txt(now_hour),
                make_exceed_txt([c for c in compared_results if c.is_exceed_thd]),
                make_unexceed_txt([c for c in compared_results if not c.is_exceed_thd]),
                footer_txt,
            ]
            if s != ""
        ]
    )
