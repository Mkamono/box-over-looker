import statistics
from datetime import datetime

from models import Analysis, Product, ScrapingResults


def make_analysis_list(
    scraping_results: ScrapingResults,
) -> list[Analysis]:
    scraping_datetime = scraping_results.scraping_results[0].date

    def calc_price_median_by_product(
        product: Product, scraping_results: ScrapingResults
    ) -> float:
        items = ScrapingResults(
            scraping_results=[
                item
                for item in scraping_results.scraping_results
                if item.product == product
            ]
        )

        prices: list[float] = [
            item.price for item in items.scraping_results if item.price is not None
        ]
        median = statistics.median(prices)
        return median

    analysis_list = [
        Analysis(
            date=scraping_datetime,
            product=product,
            median=calc_price_median_by_product(product, scraping_results),
        )
        for product in Product
    ]

    return analysis_list


def calc_average_median_price(
    analysis_list: list[Analysis], product: Product, filter_date: datetime
) -> float:
    return statistics.mean(
        [
            analysis.median
            for analysis in analysis_list
            if analysis.product == product and analysis.date >= filter_date
        ]
    )
