from strategy_builder.common.constants import POSITION
from common.constants import LOT_SIZE


class TargetProfit:
    def get_profit(self, price_at_bid, ltp, position):
        if position == POSITION.SELL.value:
            return (price_at_bid - ltp) * LOT_SIZE
        else:
            return (ltp - price_at_bid) * LOT_SIZE

    def is_target_profit_reached(self, position, leg_bid_price=None, underlying_price_at_bid=None, ltp=None, underlying_ltp=None):
        raise NotImplementedError("Subclasses must implement this method")


class TargetProfitPoints:
    pass


class TargetProfitUnderlyingPoints:
    pass


class TargetProfitPercent(TargetProfit):
    def __init__(self, value):
        self.target_profit_percent = value

    def is_target_profit_reached(self, position, leg_bid_price=None, underlying_price_at_bid=None, ltp=None, underlying_ltp=None):
        profit = self.get_profit(leg_bid_price, ltp, position)
        profit_percent = (profit * 100) / leg_bid_price
        return profit_percent > self.target_profit_percent


class TargetProfitUnderlyingPercent(TargetProfit):
    def __init__(self, value):
        self.target_profit_underlying_percent = value

    def is_target_profit_reached(self, position, leg_bid_price=None, underlying_price_at_bid=None, ltp=None, underlying_ltp=None):
        profit = self.get_profit(underlying_price_at_bid, underlying_ltp, position)
        profit_percent = (profit * 100) / underlying_ltp
        return profit_percent > self.target_profit_underlying_percent


class TargetProfitFactory:
    @staticmethod
    def create_target_profit_instance(target_profit_type, value):
        if target_profit_type == "percent":
            return TargetProfitPercent(value)
        elif target_profit_type == "underlying_percent":
            return TargetProfitUnderlyingPercent(value)
        else:
            raise ValueError("Invalid stop loss type")
