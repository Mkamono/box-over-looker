import statistics
from datetime import datetime, timedelta

from db import RangeDatetime, read_analysis_by_datetime
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
    db_name: str, product: Product, datetime_range: RangeDatetime
) -> float:
    analysis_record_list = read_analysis_by_datetime(
        db_name, datetime_range=datetime_range
    )

    return statistics.mean(
        [
            analysis.to_analysis().median
            for analysis in analysis_record_list
            if analysis.to_analysis().product == product
        ]
    )


def get_current_median_price(
    db_name: str, product: Product, datetime_range: RangeDatetime
) -> float:
    analysis_record_list = read_analysis_by_datetime(
        db_name, datetime_range=datetime_range
    )
    analysis_list = [
        analysis.to_analysis()
        for analysis in analysis_record_list
        if analysis.to_analysis().product == product
    ]
    analysis_list.sort(key=lambda x: x.date, reverse=True)
    return analysis_list[0].median
