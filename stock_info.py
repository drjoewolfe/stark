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

    def merge(self, info):
        if self.symbol != info.symbol:
            return

        # Merged only if local value is None
        self.name = info.name if self.name is None else self.name
        self.sector = info.sector if self.sector is None else self.sector
        self.price = info.price if self.price is None else self.price
        self.day_open_price = info.day_open_price if self.day_open_price is None else self.day_open_price
        self.day_previous_close_price = info.day_previous_close_price if self.day_previous_close_price is None else self.day_previous_close_price
        self.volume = info.volume if self.volume is None else self.volume
        self.value_lakhs = info.value_lakhs if self.value_lakhs is None else self.value_lakhs
        self.vwap = info.vwap if self.vwap is None else self.vwap
        self.beta = info.beta if self.beta is None else self.beta
        self.day_high_price = info.day_high_price if self.day_high_price is None else self.day_high_price
        self.day_low_price = info.day_low_price if self.day_low_price is None else self.day_low_price
        self.uc_limit = info.uc_limit if self.uc_limit is None else self.uc_limit
        self.lc_limit = info.lc_limit if self.lc_limit is None else self.lc_limit
        self.week_52_high = info.week_52_high if self.week_52_high is None else self.week_52_high
        self.week_52_low = info.week_52_low if self.week_52_low is None else self.week_52_low
        self.ttm_eps = info.ttm_eps if self.ttm_eps is None else self.ttm_eps
        self.ttm_pe = info.ttm_pe if self.ttm_pe is None else self.ttm_pe
        self.sector_pe = info.sector_pe if self.sector_pe is None else self.sector_pe
        self.book_value_per_share = info.book_value_per_share if self.book_value_per_share is None else self.book_value_per_share
        self.pb = info.pb if self.pb is None else self.pb
        self.face_value = info.face_value if self.face_value is None else self.face_value
        self.market_cap_crores = info.market_cap_crores if self.market_cap_crores is None else self.market_cap_crores
        self.dividend_yeild = info.dividend_yeild if self.dividend_yeild is None else self.dividend_yeild
        self.avg_volume_20D = info.avg_volume_20D if self.avg_volume_20D is None else self.avg_volume_20D
        self.avg_delivery_percent_20D = info.avg_delivery_percent_20D if self.avg_delivery_percent_20D is None else self.avg_delivery_percent_20D

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