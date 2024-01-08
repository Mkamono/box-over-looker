from statistics import median

from models import Analysis, Product, ScrapingResults


def create_median_list_every_product(
    single_scraping_results: ScrapingResults,
) -> list[Analysis]:
    """
    スクレイピング一回収集分のデータから各商品ごとの中央値を計算し、リストにして返す。

    ----------
    scraping_date: datetime
        データ収集日時。データの１つ目の日時を代表値とし、分、秒、マイクロ秒は切り捨てる。
    ----------

    """
    scraping_date = single_scraping_results.scraping_results[0].date.replace(
        minute=0, second=0, microsecond=0
    )
    median_list_every_product: list[Analysis] = [
        Analysis(
            date=scraping_date,
            product=product,
            median=calc_median(
                ScrapingResults(
                    scraping_results=[
                        item
                        for item in single_scraping_results.scraping_results
                        if item.product == product
                    ]
                )
            ),
        )
        for product in Product
    ]

    return median_list_every_product


def calc_median(Items: ScrapingResults) -> float:
    price_list: list[float] = [
        item.price for item in Items.scraping_results if item.price is not None
    ]
    if len(price_list) == 0:
        raise ValueError("scraping_result's value is empty")

    median_value = median(price_list)
    return median_value
