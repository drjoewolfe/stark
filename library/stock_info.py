class StockInfo:
    def __init__(self):
        self.symbol = None
        self.name = None
        self.sector = None
        self.price = None
        self.day_open_price = None
        self.day_previous_close_price = None
        self.volume = None
        self.value_lakhs = None
        self.vwap = None
        self.beta = None
        self.day_high_price = None
        self.day_low_price = None
        self.uc_limit = None
        self.lc_limit = None
        self.week_52_high = None
        self.week_52_low = None
        self.ttm_eps = None
        self.ttm_pe = None
        self.sector_pe = None
        self.sector_pb = None
        self.sector_dividend_yield = None
        self.book_value_per_share = None
        self.pb = None
        self.face_value = None
        self.market_cap_crores = None
        self.dividend_yield = None
        self.avg_volume_20D = None
        self.avg_delivery_percent_20D = None
        self.tt_intrinsic_value_commentary = None
        self.tt_returns_vs_fd_rates_commentary = None
        self.tt_dividend_returns_commentary = None
        self.tt_entry_pont_commentary = None
        self.tt_red_flags_commentary = None

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
        self.sector_pb = info.sector_pb if self.sector_pb is None else self.sector_pb
        self.sector_dividend_yield = info.sector_dividend_yield if self.sector_dividend_yield is None else self.sector_dividend_yield
        self.book_value_per_share = info.book_value_per_share if self.book_value_per_share is None else self.book_value_per_share
        self.pb = info.pb if self.pb is None else self.pb
        self.face_value = info.face_value if self.face_value is None else self.face_value
        self.market_cap_crores = info.market_cap_crores if self.market_cap_crores is None else self.market_cap_crores
        self.dividend_yield = info.dividend_yield if self.dividend_yield is None else self.dividend_yield
        self.avg_volume_20D = info.avg_volume_20D if self.avg_volume_20D is None else self.avg_volume_20D
        self.avg_delivery_percent_20D = info.avg_delivery_percent_20D if self.avg_delivery_percent_20D is None else self.avg_delivery_percent_20D
        self.tt_intrinsic_value_commentary = info.tt_intrinsic_value_commentary if self.tt_intrinsic_value_commentary is None else self.tt_intrinsic_value_commentary
        self.tt_returns_vs_fd_rates_commentary = info.tt_returns_vs_fd_rates_commentary if self.tt_returns_vs_fd_rates_commentary is None else self.tt_returns_vs_fd_rates_commentary
        self.tt_dividend_returns_commentary = info.tt_dividend_returns_commentary if self.tt_dividend_returns_commentary is None else self.tt_dividend_returns_commentary
        self.tt_entry_pont_commentary = info.tt_entry_pont_commentary if self.tt_entry_pont_commentary is None else self.tt_entry_pont_commentary
        self.tt_red_flags_commentary = info.tt_red_flags_commentary if self.tt_red_flags_commentary is None else self.tt_red_flags_commentary

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
               + "sector_pb:" + str(self.sector_pb) + ", " \
               + "sector_dividend_yield:" + str(self.sector_dividend_yield) + ", " \
               + "book_value_per_share:" + str(self.book_value_per_share) + ", " \
               + "pb:" + str(self.pb) + ", " \
               + "face_value:" + str(self.face_value) + ", " \
               + "market_cap_crores:" + str(self.market_cap_crores) + ", " \
               + "dividend_yeild:" + str(self.dividend_yield) + ", " \
               + "avg_volume_20D:" + str(self.avg_volume_20D) + ", " \
               + "avg_delivery_percent_20D:" + str(self.avg_delivery_percent_20D) + ", " \
               + "tt_intrinsic_value_commentary:" + str(self.tt_intrinsic_value_commentary) + ", " \
               + "tt_returns_vs_fd_rates_commentary:" + str(self.tt_returns_vs_fd_rates_commentary) + ", " \
               + "tt_dividend_returns_commentary:" + str(self.tt_dividend_returns_commentary) + ", " \
               + "tt_entry_pont_commentary:" + str(self.tt_entry_pont_commentary) + ", " \
               + "tt_red_flags_commentary:" + str(self.tt_red_flags_commentary) \
               + " }"
