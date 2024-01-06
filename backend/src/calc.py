from uuid import uuid4

from models import AnalysisRecord, Product, ScrapingResults


def to_analysis_records(scraping_results: ScrapingResults) -> list[AnalysisRecord]:
    analysis_records: list[AnalysisRecord] = []

    for product in Product:
        analysis_records.append(
            AnalysisRecord(
                ID=str(uuid4()),
                date=scraping_results.scraping_results[0].date.replace(
                    minute=0, second=0, microsecond=0
                ),
                median=calc_median(product, scraping_results),
                product=product,
            )
        )

    return analysis_records


def calc_median(product: Product, results: ScrapingResults) -> float:
    price_list: list[float] = []
    for item in results.scraping_results:
        if item.product == product:
            price_list.append(item.Item.price)

    price_list.sort()

    if len(price_list) == 0:
        raise ValueError("scrapping_results is empty.")
    elif len(price_list) % 2 == 0:
        median: float = (
            price_list[len(price_list) // 2] + price_list[len(price_list) // 2 - 1]
        ) / 2
    else:
        median: float = price_list[len(price_list) // 2]

    return median
