from enum import Enum

class INDEX:
    NIFTY = "nifty"
    BANKNIFTY = "banknifty"
    FINNIFTY = "finnifty"
    MIDCAPNIFTY = "midcapnifty"
    SENSEX = "sensex"
    BANKEX = "bankex"


class UNDERLYING_FORM:
    CASH = "cash"
    FUTURES = "futures"


class STRATEGY_TYPE(Enum):
    INTRADAY = "intraday"
    BTST = "btst"
    POSITIONAL = "positional"


class POSITION(Enum):
    BUY = "buy",
    SELL = "sell"


class OPTION_TYPE(Enum):
    CALL = "call"
    PUT = "put"


class EXPIRY:
    WEEKLY = "weekly"
    NEXT_WEEKLY = "next_weekly"
    MONTHLY = "monthly"


class STRIKE_CRITERIA(Enum):
    STRIKE_TYPE = "strike_type"
    PREMIUM_RANGE = "premium_range"
    CLOSEST_PREMIUM = "closest_premium"
    PREMIUM_GREATER_THAN_EQUAL = ""
    PREMIUM_LESS_THAN_EQUAL = "premium_greater_than_equal"
    STRADDLE_WIDTH = "straddle_width"
    PERCENT_OF_ATM = "percent_of_atm"
    SYNTHETIC_FUTURE = "synthetic_future"
    ATM_STRADDLE_PREMIUM_PERCENT = "atm_straddle_premium_percent"


class NUMBER_OF_SHARES_PER_LOT(Enum):
    NIFTY = 50
    FINNIFTY = 50
    SENSEX = 50
    MIDCPNIFTY = 50
    BANKNIFTY = 50
    BANKEX = 50


STRIKE_PRICE_DELTA = 50

