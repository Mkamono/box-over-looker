import statistics

from models import Analysis, Product, ScrapingResults


def make_analysis_list_every_product(
    scraping_results: ScrapingResults,
) -> list[Analysis]:
    scraping_datetime = scraping_results.scraping_results[0].date

    def calc_price_median_by_product(
        product: Product, scraping_results: ScrapingResults
    ) -> float:
        return calc_price_median(
            ScrapingResults(
                scraping_results=[
                    item
                    for item in scraping_results.scraping_results
                    if item.product == product
                ]
            )
        )

    analysis_list_every_product = [
        Analysis(
            date=scraping_datetime,
            product=product,
            median=calc_price_median_by_product(product, scraping_results),
        )
        for product in Product
    ]

    return analysis_list_every_product


def calc_price_median(Items: ScrapingResults) -> float:
    price_list: list[float] = [
        item.price for item in Items.scraping_results if item.price is not None
    ]
    median = statistics.median(price_list)
    return median
