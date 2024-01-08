import statistics

from models import Analysis, Product, ScrapingResults


def make_median_list_every_product(
    single_exec_scraping_results: ScrapingResults,
) -> list[Analysis]:
    """
    スクレイピング一回収集分の商品データから各商品ごとの中央値を計算して、リスト形式で返します。

    Parameters:
    single_exec_scraping_results (ScrapingResults): 一回分のスクレイピングによる商品データ

    Returns:
    list[Analysis]: 各製品の価格中央値を含むAnalysisオブジェクトのリスト。
    """

    scraping_datetime = single_exec_scraping_results.scraping_results[0].date.replace(
        minute=0, second=0, microsecond=0
    )
    median_list_every_product = [
        Analysis(
            date=scraping_datetime,
            product=product,
            median=calc_price_median_by_product(product, single_exec_scraping_results),
        )
        for product in Product
    ]

    return median_list_every_product


def calc_price_median_by_product(
    product: Product, single_exec_scraping_results: ScrapingResults
) -> float:
    return calc_price_median(
        ScrapingResults(
            scraping_results=[
                item
                for item in single_exec_scraping_results.scraping_results
                if item.product == product
            ]
        )
    )


def calc_price_median(Items: ScrapingResults) -> float:
    price_list: list[float] = [
        item.price for item in Items.scraping_results if item.price is not None
    ]
    median = statistics.median(price_list)
    return median
