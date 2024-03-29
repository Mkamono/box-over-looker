from urllib.parse import quote

from models import Product


class URL:
    def __init__(
        self,
        product: Product,
        price_min: int = 1000,
        price_max: int = 1000000,
        exclude_keywords: list[str] = [],
    ) -> None:
        """URLを生成するクラスです

        Args:
            product (Product): 商品名です。
            price_min (int, optional): 商品価格の下限値です。検索対象ではないパック商品を除外するため Defaults to 1000.
            price_max (int, optional): 商品価格の上限値です。いたずら出品を除外するため Defaults to 1000000.
            exclude_keywords (list[str], optional): 除外したいキーワードです。 Defaults to [].
        """
        self.product = product
        self.keywords: list[str] = [product.name, "1box", "シュリンク付き"]
        self.price_min = price_min
        self.price_max = price_max
        self.exclude_keywords = exclude_keywords

    def paypay(self, page: int) -> str:
        return f"https://paypayfleamarket.yahoo.co.jp/search/{quote(' '.join(self.keywords))}?minPrice={self.price_min}&maxPrice={self.price_max}&open=1&page={page}"

    # paypay条件　商品の状態：全て　販売状況：販売中　並び順：デフォルト（設定無し）

    def mercari(self, page: int) -> str:
        return f"https://jp.mercari.com/search?keyword={quote(' '.join(self.keywords))}&exclude_keywords={quote(' '.join(self.exclude_keywords))}&price_max={self.price_max}&price_min={self.price_min}&item_condition_id=1%2C2%2C3%2C4%2C5%2C6&status=on_sale&page_token=v1%3A{page-1}"

    # mercari条件　商品の状態：全て　販売状況：販売中　並び順：おすすめ順

    def rakuma(self, page: int) -> str:
        return f"https://fril.jp/s?query={quote(' '.join(self.keywords))}&excluded_query={quote(' '.join(self.exclude_keywords))}&min={self.price_min}&max={self.price_max}&transaction=selling&sort=sell_price&order=asc&page={page}"

    # rakuma条件　商品の状態：全て　販売状況：販売中　並び順：価格の安い順　配送オプション：全て　公式ショップ：全て　配送料の負担：全て

    def yahoo(self, page: int) -> str:
        item_display_number: int = 50
        # 1ページに表示できる商品数
        return f"https://auctions.yahoo.co.jp/search/search?min={self.price_min}&max={self.price_max}&price_type=currentprice&p={quote(' '.join(self.keywords))}&b={(page-1)*item_display_number+1}&n={item_display_number}"

    # yahoo条件　商品の状態：指定無し　価格：現在価格　並び順：おすすめ順（デフォルト）　出品者：指定無し　出品地域：指定無し

    def amazon(self, page: int) -> str:
        return f"https://kakaku.com/search_results/{quote(' '.join(self.keywords), encoding='shift-jis')}/?minp={self.price_min}&maxp={self.price_max}&mall=6&page={page}"

    # amazon条件　並び順：標準（デフォルト）　モールの指定：クエリでmall=6にするとアマゾンのみの検索になる

    def rakuten(self, page: int) -> str:
        return f"https://kakaku.com/search_results/{quote(' '.join(self.keywords), encoding='shift-jis')}/?minp={self.price_min}&maxp={self.price_max}&mall=1&page={page}"

    # 楽天市場条件　並び順：標準（デフォルト）　モールの指定：クエリでmall=1にすると楽天市場のみの検索になる

    def yshop(self, page: int) -> str:
        return f"https://kakaku.com/search_results/{quote(' '.join(self.keywords), encoding='shift-jis')}/?minp={self.price_min}&maxp={self.price_max}&mall=2&page={page}"

    # ヤフーショッピング条件　並び順：標準（デフォルト）　モールの指定：クエリでmall=2にするとヤフーショッピングのみの検索になる
