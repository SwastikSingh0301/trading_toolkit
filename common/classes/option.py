class Option:
    def __init__(self, option):
        if not option:
            raise ValueError("option cannot be empty")
        self.option_ticker = option["ticker"]
        self.option_strike_price = option["strike_price"]
        self.option_expiry_date = option["expiry_date"]
        self.option_expiry_type = option["expiry_type"]
        self.option_time = option["time"]
        self.option_datetime = option["datetime"]
        self.option_ltp = option["ltp"]


    @property
    def ltp(self):
        return self.option_ltp
