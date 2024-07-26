import os


class INDEX:
    NIFTY = "nifty"
    BANKNIFTY = "banknifty"
    FINNIFTY = "finnifty"
    MIDCAPNIFTY = "midcapnifty"
    SENSEX = "sensex"
    BANKEX = "bankex"


class LEG_STATUS:
    PENDING = "pending"
    ACTIVE = "active"
    SQUARED_OFF = "squared_off"
    INACTIVE = "inactive"
    EXITED = "exited"
    FAILED = "failed"
    RE_ENTERED = "re_entered"
    RE_EXITED = "re_exited"

class STRATEGY_STATUS:
    PENDING = "pending"
    RUNNING = "running"
    EXITED = "exited"
    RE_ENTERED = "re_entered"

class OVERALL_STOP_LOSS_TYPES:
    MAX_LOSS = "max_loss"
    TOTAL_PREMIUM_PERCENT = "total_premium_percent"

class OVERALL_TARGET_PROFIT_TYPES:
    MAX_PROFIT = "max_profit"
    TOTAL_PREMIUM_PERCENT = "total_premium_percent"


PROJECT_HOME = "/Users/swastiksingh/Personal/trading_setup/"
NIFTY_HISTORICAL_DATA = os.path.join(PROJECT_HOME, "static/nifty")
BANKNIFTY_HISTORICAL_DATA = os.path.join(PROJECT_HOME, "static/banknifty")

RABBITMQ_QUEUE_NAME = "testing_queue"
RABBITMQ_HOST = "localhost"
RABBITMQ_TRADE_QUEUE = "trade_testing_queue"

DATA_PATH = os.path.join(PROJECT_HOME, "static")

LOT_SIZE = {
    "nifty": 25,
    "banknifty": 25,
    "finnifty": 25,
    "midcapnifty": 25,
    "sensex": 25,
    "bankex": 25
}