import os


class INDEX:
    NIFTY = "nifty"
    BANKNIFTY = "banknifty"
    FINNIFTY = "finnifty"
    MIDCAPNIFTY = "midcapnifty"
    SENSEX = "sensex"
    BANKEX = "bankex"


PROJECT_HOME = "/Users/swastiksingh/Personal/trading_setup/"
NIFTY_HISTORICAL_DATA = os.path.join(PROJECT_HOME, "static/nifty")
BANKNIFTY_HISTORICAL_DATA = os.path.join(PROJECT_HOME, "static/banknifty")

RABBITMQ_QUEUE_NAME = "testing_queue"
RABBITMQ_HOST = "localhost"

