class StockInfo:
    symbol = None
    name = None
    sector = None
    price = None
    day_open_price = None
    day_previous_close_price = None
    volume = None
    value_lakhs = None
    vwap = None
    beta = None
    day_high_price = None
    day_low_price = None
    uc_limit = None
    lc_limit = None
    week_52_high = None
    week_52_low = None
    ttm_eps = None
    ttm_pe = None
    sector_pe = None
    book_value_per_share = None
    pb = None
    face_value = None
    market_cap_crores = None
    dividend_yeild = None
    avg_volume_20D = None
    avg_delivery_percent_20D = None

    def __init__(self):
        pass

    def __str__(self):
        return "{ " \
               + "symbol: " + self.symbol + ", " \
               + "name: " + self.name + ", " \
               + "sector: " + self.sector + ", " \
               + "price: " + str(self.price) + ", " \
               + "day_open_price: " + str(self.day_open_price) + ", " \
               + "day_previous_close_price:" + str(self.day_previous_close_price) + ", " \
               + "volume:" + str(self.volume) + ", " \
               + "value_lakhs:" + str(self.value_lakhs) + ", " \
               + "vwap:" + str(self.vwap) + ", " \
               + "beta:" + str(self.beta) + ", " \
               + "day_high_price:" + str(self.day_high_price) + ", " \
               + "day_low_price:" + str(self.day_low_price) + ", " \
               + "uc_limit:" + str(self.uc_limit) + ", " \
               + "lc_limit:" + str(self.lc_limit) + ", " \
               + "week_52_high:" + str(self.week_52_high) + ", " \
               + "week_52_low:" + str(self.week_52_low) + ", " \
               + "ttm_eps:" + str(self.ttm_eps) + ", " \
               + "ttm_pe:" + str(self.ttm_pe) + ", " \
               + "sector_pe:" + str(self.sector_pe) + ", " \
               + "book_value_per_share:" + str(self.book_value_per_share) + ", " \
               + "pb:" + str(self.pb) + ", " \
               + "face_value:" + str(self.face_value) + ", " \
               + "market_cap_crores:" + str(self.market_cap_crores) + ", " \
               + "dividend_yeild:" + str(self.dividend_yeild) + ", " \
               + "avg_volume_20D:" + str(self.avg_volume_20D) + ", " \
               + "avg_delivery_percent_20D:" + str(self.avg_delivery_percent_20D) + " }"
