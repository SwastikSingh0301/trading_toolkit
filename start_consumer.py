import asyncio

# from strategy_caller.strategy_caller import MessageConsumer, StrategyCaller
#
#
# class Deploy:
#     def __init__(self):
#         message_consumer_object = MessageConsumer()
#         message_consumer_object.start_consuming()
#
#
# Deploy()

from strategy_executor import strategy_executor


class Deploy:
    def __init__(self):
        strategy_executor.delay("1", "nifty", "backtest", start_date="2016-01-01", end_dat="2016-01-01")

        print("abcd")


Deploy()