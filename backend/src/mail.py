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


def make_mail_body(compared_results: list[ComparedResult]) -> str:
    user_config = get_user_config()
    # 一番初めの文を作成。これに追加していく。
    body: str = "本日の0時時点での取引価格によるお知らせです。\n"

    def make_body_by_product(compared_result: ComparedResult) -> str:
        if compared_result.is_exceed_thd:
            price_change_word: str = "上昇"
            word_exceed_thd: str = "急激な価格の上昇が起きています。"
        if compared_result.increase_price_percentage > 0:
            price_change_word: str = "上昇"
            word_exceed_thd: str = ""
        else:
            price_change_word: str = "減少"
            word_exceed_thd: str = ""

        # 1つの商品分の本文を作成する
        body = f"・{compared_result.product}。\n現在の取引価格は約{compared_result.current_price}円です。{word_exceed_thd}過去{user_config.period_days}日間の平均価格と比較して、{compared_result.increase_price_percentage}%{price_change_word}しています。\n"

        return body

    def make_body_core(compared_results: list[ComparedResult]) -> str:
        results_exceed_thd: list[ComparedResult] = [
            compared_result
            for compared_result in compared_results
            if compared_result.is_exceed_thd
        ]

        results_not_exceed_thd: list[ComparedResult] = [
            compared_result
            for compared_result in compared_results
            if not compared_result.is_exceed_thd
        ]
        # 閾値を3つとも超えているかどうかで、本文内のタイトルを変更する。
        if len(results_exceed_thd) == 0:
            title_exceed_thd: str = ""
            title_not_exceed_thd: str = "価格の急激な上昇が確認されなかった商品"
        if len(results_exceed_thd) == 3:
            title_exceed_thd: str = "価格の急激な上昇が確認された商品"
            title_not_exceed_thd: str = ""
        else:
            title_exceed_thd: str = "価格の急激な上昇が確認された商品"
            title_not_exceed_thd: str = "価格の急激な上昇が確認されなかった商品"

        body_core = f"""
{title_exceed_thd}

{"".join([make_body_by_product(result) for result in results_exceed_thd])}

{title_not_exceed_thd}

{"".join([make_body_by_product(result) for result in results_not_exceed_thd])}
"""
        return body_core

    # 本文の冒頭部分
    body_first: str = "本日の0時時点での取引価格によるお知らせです。\n"

    body_core = make_body_core(compared_results)

    body_last: str = f"""
現在の閾値は{user_config.threshold_increase_rate_price}%です。閾値の変更は、以下のURLのReadmeをお読みください。

“https://github.com/Mkamono/box-over-looker”
"""
    # URLはリポジトリ譲渡後に変更する。

    return body_first + body_core + body_last
